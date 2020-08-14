import torch
import torch.nn as nn
import torch.nn.init as init
import torch.nn.functional as F
from encoder.models.hyperparameters import Hyperparameters as hp
import numpy as np

class GST(nn.Module):

    def __init__(self,output_embedding_dim=128):
        super().__init__()
        hp.E = output_embedding_dim
        self.encoder = ReferenceEncoder(output_embedding_dim=output_embedding_dim)
        self.stl = STL(output_embedding_dim=output_embedding_dim)



    def forward(self, inputs, key_embed=None):
        enc_out = self.encoder(inputs)
        style_embed = self.stl(enc_out, key_embed)
        return style_embed



class ReferenceEncoder(nn.Module):
    '''
    inputs --- [N, Ty/r, n_mels*r]  mels
    outputs --- [N, ref_enc_gru_size]
    '''

    def __init__(self,output_embedding_dim=128):
        super().__init__()
        hp.E = output_embedding_dim
        K = len(hp.ref_enc_filters)
        filters = [1] + hp.ref_enc_filters
        convs = [nn.Conv2d(in_channels=filters[i],
                           out_channels=filters[i + 1],
                           kernel_size=(3, 3),
                           stride=(2, 2),
                           padding=(1, 1)) for i in range(K)]
        self.convs = nn.ModuleList(convs)
        self.bns = nn.ModuleList([nn.BatchNorm2d(num_features=hp.ref_enc_filters[i]) for i in range(K)])

        out_channels = self.calculate_channels(hp.n_mels, 3, 2, 1, K)
        self.gru = nn.GRU(input_size=hp.ref_enc_filters[-1] * out_channels,
                          hidden_size=hp.E // 2,
                          batch_first=True)

    def forward(self, inputs):
        N = inputs.size(0)
        out = inputs.view(N, 1, -1, hp.n_mels)  # [N, 1, Ty, n_mels]
        for conv, bn in zip(self.convs, self.bns):
            out = conv(out)
            out = bn(out)
            out = F.relu(out)  # [N, 128, Ty//2^K, n_mels//2^K]

        out = out.transpose(1, 2)  # [N, Ty//2^K, 128, n_mels//2^K]
        T = out.size(1)
        N = out.size(0)
        out = out.contiguous().view(N, T, -1)  # [N, Ty//2^K, 128*n_mels//2^K]


        self.gru.flatten_parameters()
        memory, out = self.gru(out)  # out --- [1, N, E//2]

        return out.squeeze(0)

    def calculate_channels(self, L, kernel_size, stride, pad, n_convs):
        for i in range(n_convs):
            L = (L - kernel_size + 2 * pad) // stride + 1
        return L


class STL(nn.Module):
    '''
    inputs --- [N, E//2]
    '''

    def __init__(self,output_embedding_dim=128):
        super().__init__()
        hp.E = output_embedding_dim

        # token_embed = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]).T ## This gets re-written by token keys from trained model, so it has to be done in forward()
        # token_embed = np.tile(token_embed, (1, hp.E // hp.num_heads))
        # self.embed = nn.Parameter(torch.FloatTensor(token_embed))

        self.embed = nn.Parameter(torch.FloatTensor(hp.token_num, hp.E // hp.num_heads))
        d_q = hp.E // 2
        d_k = hp.E // hp.num_heads
        # self.attention = MultiHeadAttention(hp.num_heads, d_model, d_q, d_v)
        self.attention = MultiHeadAttention(query_dim=d_q, key_dim=d_k, num_units=hp.E, num_heads=hp.num_heads)

        init.normal_(self.embed, mean=0, std=0.5)



    def forward(self, inputs, key_embed):
        N = inputs.size(0)
        query = inputs.unsqueeze(1)  # [N, 1, E//2]

        if(key_embed is not None):
            key_embed = nn.Parameter(torch.FloatTensor(np.tile(key_embed, (1, hp.E // hp.num_heads))).cuda())
            style_control_embed = self.embed * key_embed
        else:
            style_control_embed = self.embed

        keys = F.tanh(style_control_embed).unsqueeze(0).expand(N, -1, -1)  # [N, token_num, E // num_heads]
        style_embed = self.attention(query, keys)

        return style_embed


class MultiHeadAttention(nn.Module):
    '''
    input:
        query --- [N, T_q, query_dim]
        key --- [N, T_k, key_dim]
    output:
        out --- [N, T_q, num_units]
    '''

    def __init__(self, query_dim, key_dim, num_units, num_heads):

        super().__init__()
        self.num_units = num_units
        self.num_heads = num_heads
        self.key_dim = key_dim

        self.W_query = nn.Linear(in_features=query_dim, out_features=num_units, bias=False)
        self.W_key = nn.Linear(in_features=key_dim, out_features=num_units, bias=False)
        self.W_value = nn.Linear(in_features=key_dim, out_features=num_units, bias=False)

    def forward(self, query, key):
        querys = self.W_query(query)  # [N, T_q, num_units]
        keys = self.W_key(key)  # [N, T_k, num_units]
        values = self.W_value(key)

        split_size = self.num_units // self.num_heads
        querys = torch.stack(torch.split(querys, split_size, dim=2), dim=0)  # [h, N, T_q, num_units/h]
        keys = torch.stack(torch.split(keys, split_size, dim=2), dim=0)  # [h, N, T_k, num_units/h]
        values = torch.stack(torch.split(values, split_size, dim=2), dim=0)  # [h, N, T_k, num_units/h]

        # score = softmax(QK^T / (d_k ** 0.5))
        scores = torch.matmul(querys, keys.transpose(2, 3))  # [h, N, T_q, T_k]
        scores = scores / (self.key_dim ** 0.5)
        scores = F.softmax(scores, dim=3)

        # out = score * V
        out = torch.matmul(scores, values)  # [h, N, T_q, num_units/h]
        out = torch.cat(torch.split(out, 1, dim=0), dim=3).squeeze(0)  # [N, T_q, num_units]

        return out
