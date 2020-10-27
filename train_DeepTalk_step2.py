## Sample usage:
# Python train_DeepTalk_step2.py Data/LibriSpeech/train-other-custom/<speaker_name>

from distutils.dir_util import copy_tree
from shutil import copyfile
import os, sys
import ntpath
from synthesizer_preprocess_audio import run_custom as syn_prep_audio
from synthesizer_preprocess_embeds import run_custom as syn_prep_embeds
from synthesizer_train import run_custom as syn_train
from vocoder_preprocess import run_custom as voc_prep
from vocoder_train import run_custom as voc_train
from shutil import rmtree
import time


def main(argv):

   
    input_path = argv[0]
    speaker_name = ntpath.basename(input_path)
    data_dir = os.path.abspath('Data')
    pretrained_model_name = 'model_GST'
    finetuned_model_name = pretrained_model_name + '_ft_' + speaker_name.lower()
    pretrained_encoder_model_path = os.path.join('trained_models', speaker_name, 'Encoder', pretrained_model_name + '.pt')
    finetuned_syn_model_dir = os.path.join('trained_models', speaker_name, 'Synthesizer', 'logs-' + pretrained_model_name + '_ft')
    finetuned_voc_model_dir = os.path.join('trained_models', speaker_name, 'Vocoder')     
    syn_files_dir = os.path.join(data_dir, 'SV2TTS', 'synthesizer_' + finetuned_model_name)    
    voc_files_dir = os.path.join(data_dir, 'SV2TTS', 'vocoder_' + finetuned_model_name)

    
    
    if not os.path.exists(syn_files_dir):
        os.makedirs(syn_files_dir)
    if not os.path.exists(finetuned_syn_model_dir):
        os.makedirs(finetuned_syn_model_dir)
    if not os.path.exists(voc_files_dir):
        os.makedirs(voc_files_dir)
    if not os.path.exists(finetuned_voc_model_dir):
        os.makedirs(finetuned_voc_model_dir)

    
    ##
    # print("---------------------------------------------------------")
    # print("Step1: Initialize the trained_model directory for the finetuning process using the generic pre-trained model in the trained_models directory ")

    # generic_model_path = os.path.join('trained_models','Generic')
    # finetuned_model_path = os.path.join('trained_models', speaker_name)
    # ref_audio_output_path = os.path.join('uploads', speaker_name + '.wav')

    # sample_dirs = next(os.walk(input_path))[1] ## Get all sample directories
    # for sample_dir in sample_dirs:
    #     sample_path = os.path.join(input_path, sample_dir)
    #     for root, dirs, files in os.walk(sample_path):
    #         for filename in files:
    #             if os.path.splitext(filename)[1] == ".wav":
    #                 ref_audio_input_path = os.path.join(sample_path, filename)
    #                 copyfile(ref_audio_input_path, ref_audio_output_path)  ## Copy a sample audio to uploads directory
    #                 break
    #         break
    #     break
    
    # if not os.path.isdir(finetuned_model_path):
    #     copy_tree(generic_model_path, finetuned_model_path)
    #     os.rename(os.path.join(finetuned_model_path, 'Synthesizer', 'logs-model_GST'), os.path.join(finetuned_model_path, 'Synthesizer', 'logs-model_GST_ft'))
    #     os.rename(os.path.join(finetuned_model_path, 'Vocoder', 'model_GST'), os.path.join(finetuned_model_path, 'Vocoder', 'model_GST_ft'))
    #     os.rename(os.path.join(finetuned_model_path, 'Vocoder', 'model_GST_ft','model_GST.pt'), os.path.join(finetuned_model_path, 'Vocoder', 'model_GST_ft','model_GST_ft.pt'))
        
    print("---------------------------------------------------------")
    print("Step 5: Preprocess data for training the Vocoder")
    voc_prep(syn_files_dir, voc_files_dir, finetuned_syn_model_dir)
    print("Step 5 Complete")
    print("---------------------------------------------------------")
    print("Step 6: Finetune Vocoder")
    voc_train(pretrained_model_name + '_ft', syn_files_dir, voc_files_dir, finetuned_voc_model_dir)
    print("Step 6 Complete")
    print("---------------------------------------------------------")
    # Remove data from SV2TTS directory
    rmtree(syn_files_dir)
    rmtree(voc_files_dir)

    print("-----------------Finetuning Completed!!----------------------")


if __name__ == "__main__":
    main(sys.argv[1:])