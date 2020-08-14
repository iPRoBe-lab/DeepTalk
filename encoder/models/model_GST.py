from encoder.params_model import *
from encoder.params_data import *
from scipy.interpolate import interp1d
from sklearn.metrics import roc_curve
from torch.nn.utils import clip_grad_norm_
from scipy.optimize import brentq
from torch import nn
from encoder.models import GST as prosody_network
import numpy as np
import torch
import torch.nn.functional as F

##Parameters for fCNN

## Mel-filterbank
mel_window_length = 25  # In milliseconds
mel_window_step = 10    # In milliseconds
mel_n_channels = 128

# Audio Parameters for fCNN
sampling_rate = 8000 # For mel-spectrograms
# Number of spectrogram frames in a partial utterance
partials_n_frames = 200     # 1600 ms
# Number of spectrogram frames at inference
inference_n_frames = 100     #  800 ms

## Model parameters fCNN model
model_hidden_size = 128
model_embedding_size = 128
model_num_layers = 3

## Training parameters
learning_rate_init = 1e-4
speakers_per_batch = 32
utterances_per_speaker = 10


class SpeakerEncoder(nn.Module):
    def __init__(self, device, loss_device):
        super().__init__()
        self.loss_device = loss_device

        # Network defition
        self.fCNN = nn.Sequential(
            nn.Conv2d(1, 2, kernel_size=(5,1), dilation = (2,1)),
            nn.SELU(),

            nn.Conv2d(2, 4, kernel_size=(5,1), dilation = (2,1)),
            nn.SELU(),

            nn.Conv2d(4, 8, kernel_size=(7,1), dilation = (3,1)),
            nn.SELU(),

            nn.Conv2d(8, 16, kernel_size=(9,1), dilation = (4,1)),
            nn.SELU(),

            nn.Conv2d(16, 32, kernel_size=(11,1), dilation = (5,1)),
            nn.SELU(),
            nn.ZeroPad2d((0, 0, 3, 4)),
            nn.Conv2d(32, 40, kernel_size=(11,1), dilation = (5,1)),
            nn.SELU()
        ).to(device)

        self.OneDCNN = nn.Sequential(

            nn.ZeroPad2d((0, 0, 2, 2)),
            nn.Conv2d(1, 16, kernel_size=(3,1), stride=1, padding=0 , dilation = (2,1)),
            nn.SELU(),

            nn.Conv2d(16, 32, kernel_size=(3,1), stride=1, padding=0, dilation = (2,1)),
            nn.SELU(),

            nn.Conv2d(32, 64, kernel_size=(7,1), padding=0, dilation = (2,1)),
            nn.SELU(),

            nn.ZeroPad2d((0, 0, 0, 1)),
            nn.Conv2d(64, 128, kernel_size=(9,1), stride=1, dilation = (3,1)),
            nn.SELU()
        ).to(device)

        self.gst = prosody_network.GST(output_embedding_dim=256).to(device)

        self.temporal_aggregation = nn.Sequential(
            nn.AvgPool2d(kernel_size=(1,partials_n_frames))
        ).to(device)

        self.regularization = nn.Sequential(
            nn.AlphaDropout(p=0.30),
        ).to(device)

        self.lstm = nn.LSTM(input_size=mel_n_channels,
                            hidden_size=model_hidden_size,
                            num_layers=model_num_layers,
                            batch_first=True).to(device)
        self.linear = nn.Linear(in_features=model_hidden_size,
                                out_features=model_embedding_size).to(device)
        self.relu = torch.nn.ReLU().to(device)
        self.selu = torch.nn.SELU().to(device)

        # Cosine similarity scaling (with fixed initial parameter values)
        self.similarity_weight = nn.Parameter(torch.tensor([10.])).to(loss_device)
        self.similarity_bias = nn.Parameter(torch.tensor([-5.])).to(loss_device)

        # Loss
        self.loss_fn = nn.CrossEntropyLoss().to(loss_device)

    def do_gradient_ops(self):
        # Gradient scale
        self.similarity_weight.grad *= 0.01
        self.similarity_bias.grad *= 0.01

        # Gradient clipping
        clip_grad_norm_(self.parameters(), 3, norm_type=2)


    def forward(self, utterances, hidden_init=None, **kwargs):
        """
        Computes the embeddings of a batch of utterance spectrograms.

        :param utterances: batch of mel-scale filterbanks of same duration as a tensor of shape
        (batch_size, n_frames, n_channels)
        :param hidden_init: initial hidden state of the LSTM as a tensor of shape (num_layers,
        batch_size, hidden_size). Will default to a tensor of zeros if None.
        :return: the embeddings as a tensor of shape (batch_size, embedding_size)
        """
        # Pass the input through the LSTM layers and retrieve all outputs, the final hidden state
        # and the final cell state.

        if 'key_embed' in kwargs:
            key_embed = kwargs.get('key_embed')
        else:
            key_embed = None

        ## Only 1D-Triplet-CNN(fCNN)
        utterances = utterances.unsqueeze(1)
        utterances = utterances.permute(0,1,3,2)
        fCNN_ftr = self.fCNN(utterances.float())
        fCNN_ftr = fCNN_ftr.squeeze(2)

        ## GST on of fCNN features
        fCNN_ftr = fCNN_ftr.permute(0,2,1)
        embeds_style = self.gst(fCNN_ftr, key_embed)
        embeds_style = embeds_style.squeeze(1)


        # L2-normalize it
        embeds = F.normalize(embeds_style, p=2, dim=1)


        return embeds

    def similarity_matrix(self, embeds):
        """
        Computes the similarity matrix according the section 2.1 of GE2E.

        :param embeds: the embeddings as a tensor of shape (speakers_per_batch,
        utterances_per_speaker, embedding_size)
        :return: the similarity matrix as a tensor of shape (speakers_per_batch,
        utterances_per_speaker, speakers_per_batch)
        """
        speakers_per_batch, utterances_per_speaker = embeds.shape[:2]

        # Inclusive centroids (1 per speaker). Cloning is needed for reverse differentiation
        centroids_incl = torch.mean(embeds, dim=1, keepdim=True)
        centroids_incl = centroids_incl.clone() / torch.norm(centroids_incl, dim=2, keepdim=True)

        # Exclusive centroids (1 per utterance)
        centroids_excl = (torch.sum(embeds, dim=1, keepdim=True) - embeds)
        centroids_excl /= (utterances_per_speaker - 1)
        centroids_excl = centroids_excl.clone() / torch.norm(centroids_excl, dim=2, keepdim=True)

        # Similarity matrix. The cosine similarity of already 2-normed vectors is simply the dot
        # product of these vectors (which is just an element-wise multiplication reduced by a sum).
        # We vectorize the computation for efficiency.
        sim_matrix = torch.zeros(speakers_per_batch, utterances_per_speaker,
                                 speakers_per_batch).to(self.loss_device)
        mask_matrix = 1 - np.eye(speakers_per_batch, dtype=np.int)
        for j in range(speakers_per_batch):
            mask = np.where(mask_matrix[j])[0]
            sim_matrix[mask, :, j] = (embeds[mask] * centroids_incl[j]).sum(dim=2)
            sim_matrix[j, :, j] = (embeds[j] * centroids_excl[j]).sum(dim=1)

        ## Even more vectorized version (slower maybe because of transpose)
        # sim_matrix2 = torch.zeros(speakers_per_batch, speakers_per_batch, utterances_per_speaker
        #                           ).to(self.loss_device)
        # eye = np.eye(speakers_per_batch, dtype=np.int)
        # mask = np.where(1 - eye)
        # sim_matrix2[mask] = (embeds[mask[0]] * centroids_incl[mask[1]]).sum(dim=2)
        # mask = np.where(eye)
        # sim_matrix2[mask] = (embeds * centroids_excl).sum(dim=2)
        # sim_matrix2 = sim_matrix2.transpose(1, 2)

        sim_matrix = sim_matrix * self.similarity_weight + self.similarity_bias
        return sim_matrix

    def loss(self, embeds):
        """
        Computes the softmax loss according the section 2.1 of GE2E.

        :param embeds: the embeddings as a tensor of shape (speakers_per_batch,
        utterances_per_speaker, embedding_size)
        :return: the loss and the EER for this batch of embeddings.
        """
        speakers_per_batch, utterances_per_speaker = embeds.shape[:2]

        # Loss
        sim_matrix = self.similarity_matrix(embeds)
        sim_matrix = sim_matrix.reshape((speakers_per_batch * utterances_per_speaker,
                                         speakers_per_batch))
        ground_truth = np.repeat(np.arange(speakers_per_batch), utterances_per_speaker)
        target = torch.from_numpy(ground_truth).long().to(self.loss_device)
        loss = self.loss_fn(sim_matrix, target)

        # EER (not backpropagated)
        with torch.no_grad():
            inv_argmax = lambda i: np.eye(1, speakers_per_batch, i, dtype=np.int)[0]
            labels = np.array([inv_argmax(i) for i in ground_truth])
            preds = sim_matrix.detach().cpu().numpy()

            # Snippet from https://yangcha.github.io/EER-ROC/
            fpr, tpr, thresholds = roc_curve(labels.flatten(), preds.flatten())
            eer = brentq(lambda x: 1. - x - interp1d(fpr, tpr)(x), 0., 1.)

        return loss, eer
