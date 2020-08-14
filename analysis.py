# Reset workspace (optional)
# print('Resetting python workspace ...')
# from IPython import get_ipython
# get_ipython().magic('reset -sf')

## Set the current working directory
import sys, os
import numpy as np
# os.chdir('/scratch0/chowdh51/Code/DeepTalk/Deployment')
# #
# print(os.getcwd())

from demo_functions import *

from IPython.display import Audio
import librosa as lr
from tqdm import tqdm

# ref_audio_path='samples/ref_VCTKp240.wav'
# output_text = 'The Norsemen considered the rainbow as a bridge over which the gods passed from earth to their home in the sky.'

# ref_audio_path='samples/obama_speech_ref.wav'
ref_audio_path='samples/song.wav'
output_text = 'The Norsemen considered the rainbow as a bridge over which the gods passed from earth to their home in the sky.'
output_dir = 'samples/DeepVOX_GST_analysis/'

# key_embed = None
# key_embed = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]).T
# synthesized_wav, sample_rate, embed = run_DeepTalk_demo(ref_audio_path=ref_audio_path, output_text=output_text, key_embed=key_embed)
# Audio(synthesized_wav,rate=sample_rate)



key_embed = np.array([[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]).T  ## STL keys for GST based models
# key_embed = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]).T

for i in tqdm(range(0,10)):
    dirName = output_dir+'Token_'+str(i)
    if not os.path.exists(dirName):
        os.makedirs(dirName)
    for j in np.arange(-1, 1.1,0.25):
        key_embed[i]=j+0.001
        synthesized_wav, sample_rate, embed = run_DeepTalk_demo(ref_audio_path=ref_audio_path, output_text=output_text, key_embed=key_embed)
        output_wav_path = dirName+'/'+'gen_audio_'+str(j)+'.wav'
        output_embedding_path = dirName+'/'+'ref_DeepVOX_GST_embed_'+str(j)+'.npy'
        np.save(output_embedding_path,embed)
        lr.output.write_wav(output_wav_path, synthesized_wav, sample_rate)


# Audio(synthesized_wav,rate=sample_rate)
