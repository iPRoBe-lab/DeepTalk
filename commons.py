import io

import torch
import torch.nn as nn
from torchvision import models
from PIL import Image
import torchvision.transforms as transforms
from encoder import inference as encoder
from encoder import audio
import librosa
from pathlib import Path


def get_model():
    model_save_path = Path('/scratch2/chowdh51/Code/DeepTalk/Deployment/encoder/saved_models/model_GST.pt')
    module_name = 'model_GST'
    encoder.load_model(model_save_path, module_name=module_name)
    return encoder

def get_tensor(file_path, preprocess=True, sampling_rate=8000, duration=None):
    if(preprocess):
        ref_audio = encoder.preprocess_wav(file_path)
    else:
        ref_audio, sr = librosa.load(file_path, sr=sampling_rate)

    if(duration is not None):
        ref_audio = ref_audio[0:int(duration*sampling_rate)]
    return ref_audio
