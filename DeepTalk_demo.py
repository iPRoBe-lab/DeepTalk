
print('Resetting python workspace ...')
from IPython import get_ipython
get_ipython().magic('reset -sf')

## Set the current working directory
import sys, os
import numpy as np
os.chdir('/scratch2/chowdh51/Code/DeepTalk/Deployment/')
print('Setting current working directory to ...')
print(os.getcwd())

# from encoder import inference_baseline as encoder


from encoder import audio
from pathlib import Path
import numpy as np
import argparse
import torch
import sys
from IPython.display import Audio
import librosa
import torchvision.transforms as transforms
from toolbox import Toolbox
from scipy import signal, fftpack
import scipy.spatial as sp
from demo_functions import *
## Info & args

#
# class hyperparameter:
#     def __init__(self):
#         # DeepTalk encoder (model_GST: fCNN + GST) trained on Librispeech, VoxCeleb1, and VoxCeleb2 Data
#         self.enc_model_fpath = Path('encoder/saved_models/model_GST_librispeech.pt')
#         self.enc_module_name = "model_GST"
#
#         # self.enc_model_fpath = Path('encoder/saved_models/pretrained.pt')
#         # self.enc_module_name = "model_baseline"
#
#         self.enc_model_fpath = '/scratch2/chowdh51/Code/SPL2018/trained_models/TPAMI2019/veri_oned_triplet_fcnn_online_VOX_Celeb2.pth.tar_best.pth.tar'
#         self.enc_module_name = None
#
#         # self.enc_model_fpath = '/scratch2/chowdh51/Code/SingingVoiceDataset/trained_models/veri_oned_triplet_cnn_VOX_Celeb2_GST_MFCC-LPC_online_16KHz.pth.tar_best.pth.tar'
#         # self.enc_module_name = None
#
#         self.syn_model_dir = Path('synthesizer/saved_models/logs-pretrained/taco_pretrained/')
#         self.voc_model_fpath = Path('vocoder/saved_models/pretrained/pretrained.pt')
#         self.low_mem = False        # "If True, the memory used by the synthesizer will be freed after each use. Adds large "
#                                     # "overhead but allows to save some GPU memory for lower-end GPUs."
#         self.no_sound = False       # If True, audio won't be played.
#         self.ref_audio_path = 'samples/ref_VCTKp240.wav'
#         # self.ref_audio_path = 'samples/MorganFreeman_speech_ref.wav'
#         self.sampling_rate = 8000  ## 16000: For mel-spectrogram based methods; 8000: For fCNN base methods
#         self.output_text = 'The Norsemen considered the rainbow as a bridge over which the gods passed from earth to their home in the sky.'
#
# 
#
#
# args = hyperparameter()
# # os.environ["CUDA_VISIBLE_DEVICES"] = '0'
# embedding = DeepVOX_GST_encoder(args.ref_audio_path, args.enc_model_fpath, sampling_rate=16000, n_channels=1, is_cmvn=True)
# embedding = fCNN_encoder(args.ref_audio_path, args.enc_model_fpath, sampling_rate=8000, n_channels=1, is_cmvn=True)
# embedding = DeepTalk_encoder(args.ref_audio_path, args.enc_model_fpath, args.enc_module_name, \
# preprocess=True, normalize=True, sampling_rate=args.sampling_rate, duration=None)
# # np.linalg.norm(embedding)
#
# synthesized_mel, breaks = DeepTalk_synthesizer(embedding, args.output_text, args.syn_model_dir, low_mem = args.low_mem)
# synthesized_wav = DeepTalk_vocoder(synthesized_mel, breaks, args.voc_model_fpath, normalize=True)

# output_text = "When the sunlight strikes raindrops in the air, they act as a prism and form a rainbow. The rainbow is a division of white light into many beautiful colors. These take the shape of a long round arch, with its path high above, and its two ends apparently beyond the horizon. There is , according to legend, a boiling pot of gold at one end. People look, but no one ever finds it. When a man looks for something beyond his reach, his friends say he is looking for the pot of gold at the end of the rainbow. Throughout the centuries people have explained the rainbow in various ways. Some have accepted it as a miracle without physical explanation. To the Hebrews it was a token that there would be no more universal floods. The Greeks used to imagine that it was a sign from the gods to foretell war or heavy rain. The Norsemen considered the rainbow as a bridge over which the gods passed from earth to their home in the sky. Others have tried to explain the phenomenon physically. Aristotle thought that the rainbow was caused by reflection of the sun’s rays by the rain. Since then physicists have found that it is not reflection, but refraction by the raindrops which causes the rainbows. Many complicated ideas about the rainbow have been formed. The difference in the rainbow depends considerably upon the size of the drops, and the width of the colored band increases as the size of the drops increases. The actual primary rainbow observed is said to be the effect of super-imposition of a number of bows. If the red of the second bow falls upon the green of the first, the result is to give a bow with an abnormally wide yellow band, since red and green light when mixed form yellow. This is a very common type of bow, one showing mainly red and yellow, with little or no green or blue. "

output_text = 'When the sunlight strikes raindrops in the air, they act as a prism and form a rainbow. \n The rainbow is a division of white light into many beautiful colors. \n These take the shape of a long round arch, with its path high above, and its two ends apparently beyond the horizon. \n There is , according to legend, a boiling pot of gold at one end. People look, but no one ever finds it. \n When a man looks for something beyond his reach, his friends say he is looking for the pot of gold at the end of the rainbow. \n Throughout the centuries people have explained the rainbow in various ways.'

synthesized_wav, sample_rate = run_DeepTalk_demo(ref_audio_path='samples/MorganFreeman_speech_ref.wav', output_text=output_text)

ref_audio_path = 'samples/ref_VCTKp240.wav'
output_text = 'The Norsemen considered the rainbow as a bridge over which the gods passed from earth to their home in the sky.'
synthesized_wav, sample_rate = run_DeepTalk_demo(ref_audio_path=ref_audio_path,output_text=output_text)


#
# print('Synthesized Audio: ')
sample_rate = 16000
Audio(synthesized_wav, rate = sample_rate)
# librosa.output.write_wav('samples/synthe
