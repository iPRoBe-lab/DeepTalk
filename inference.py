import json

from commons import get_model, get_tensor
import numpy as np
encoder = get_model()

def get_speaker_embedding(file_path, preprocess=True, sampling_rate=8000, duration=None, normalize=True):
    ref_audio = get_tensor(file_path, preprocess=preprocess, sampling_rate=sampling_rate, duration=duration)
    embed, partial_embeds, _  = encoder.embed_utterance(ref_audio, return_partials=True)

    if(normalize):
        embed = embed / np.linalg.norm(embed)
    return embed
