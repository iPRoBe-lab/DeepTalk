import os
from demo_functions import run_DeepTalk_demo as DeepTalk
import soundfile as sf
from pathlib import Path

## This Demo file requires the trained_models directory to be present in the same location as this file


## Set the current working directory to the path where 'DeepTalk-Deployment' directory is placed in your system
os.chdir('/scratch0/chowdh51/Code/DeepTalk-Deployment')
print(os.getcwd())


enc_module_name = "model_GST"  ## DO NOT CHANGE!


## Uncomment the block corresponding to the identity that you want to generate synthetic audios for

# ## For Generic
# ref_audio_path = 'uploads/Generic.wav'
# enc_model_fpath =  Path('trained_models/Generic/Encoder/model_GST.pt')
# syn_model_dir =  Path('trained_models/Generic/Synthesizer/logs-model_GST/taco_pretrained')
# voc_model_fpath =  Path('trained_models/Generic/Vocoder/model_GST/model_GST.pt')


# ## For Hannah
ref_audio_path = 'uploads/Hannah.wav'
enc_model_fpath =  Path('trained_models/Hannah/Encoder/model_GST.pt')
syn_model_dir =  Path('trained_models/Hannah/Synthesizer/logs-model_GST_ft/taco_pretrained')
voc_model_fpath =  Path('trained_models/Hannah/Vocoder/model_GST_ft/model_GST_ft.pt')


# ## For Ted
# ref_audio_path = 'uploads/Ted.wav'
# enc_model_fpath =  Path('trained_models/Ted/Encoder/model_GST.pt')
# syn_model_dir =  Path('trained_models/Ted/Synthesizer/logs-model_GST_ft/taco_pretrained')
# voc_model_fpath =  Path('trained_models/Ted/Vocoder/model_GST_ft/model_GST_ft.pt')


## For Gordon
# ref_audio_path = 'uploads/GordonSmith.wav'
# enc_model_fpath =  Path('trained_models/GordonSmith/Encoder/model_GST.pt')
# syn_model_dir =  Path('trained_models/GordonSmith/Synthesizer/logs-model_GST_ft/taco_pretrained')
# voc_model_fpath =  Path('trained_models/GordonSmith/Vocoder/model_GST_ft/model_GST_ft.pt')


## Edit the target_text to anything you want to be spoken out by the synthetic voice
target_text = 'Broadcast journalists are dedicated to fact-based news reporting.'

## This is where the generated synthetic audio file is saved
generated_audio_file = 'uploads/ref_gen.wav'  

## Run DeepTalk
synthesized_wav, sample_rate, _ = DeepTalk(ref_audio_path=ref_audio_path, output_text=target_text,
            enc_model_fpath=enc_model_fpath, enc_module_name=enc_module_name,
            syn_model_dir=syn_model_dir, voc_model_fpath=voc_model_fpath)

## Write output to file
sf.write(generated_audio_file, synthesized_wav, sample_rate, 'PCM_24')
