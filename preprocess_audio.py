## Sample usage:
# Python preprocess_audio.py Data/SampleAudio Data/ProcessedAudio

import sys, os
import getopt
import platform
from split_audio import split_audio_main
import subprocess as sub
from shutil import rmtree
from distutils.dir_util import copy_tree
from pathlib import Path
from parse_textgrid import parse_main

def main(argv):
   input_path = ''
   output_path = ''
   print(argv)
   
   input_path, output_path = argv[0], argv[1]

   training_data_directory = 'Data/LibriSpeech/train-other-custom'

   if (not(input_path) or not(output_path)):
       print('----------------------------------------------------')
       print('Improper usage!! Arguments missing!!')
       print('preprocess_audio.py <input_path> <output_path>')
       print('----------------------------------------------------')
       sys.exit(2)
       
    
   # Check if input path is a valid directory
   if not os.path.exists(input_path):
       print('Input directory not found!!')
       sys.exit(2)

   # Check if output path is a valid directory
   if not os.path.exists(output_path):
       os.makedirs(output_path)
       print('Output directory created!!')

   input_path = os.path.abspath(input_path)
   output_path = os.path.abspath(output_path)
   training_data_directory = os.path.abspath(training_data_directory)
   if not os.path.exists(training_data_directory):
       os.makedirs(training_data_directory)
   print('----------------------------------------------------')
   print("Stage 1: Splitting input audio into smaller chunks and extracting text transcripts")
   print('Input path is:', input_path)
   print('Output path is:', output_path)

   split_audio_main(input_path, output_path) ## Split the audio into smaller chunks and run speech recognition on them.

   print('------------------Stage 1 Complete-------------------')

   print('----------------------------------------------------')
   print("Stage 2: Run Montreal-Forced-Alignment to force-align text transcipts with speech audio at word level and generate alignment file")
   current_dir = os.getcwd()
   os_type = platform.system()
   if (os_type == 'Linux'):
       mfa_dir = os.path.abspath('montreal_forced_aligner_linux')
   elif (os_type == 'Darwin'):
       mfa_dir = os.path.abspath('montreal_forced_aligner_mac')
   else:
       print('montreal_forced_aligner not available for Windows! Please run it on a Linux distribution or Mac OSX')
      
   if os.path.exists(mfa_dir):
       os.chdir(mfa_dir)
   else:
       print(os.getcwd())
       print('montreal_forced_aligner directory not found!!')
       sys.exit(2)

   speaker_dir_path = ''

   for root, speaker_dirs, files in os.walk(output_path):
        for speaker_dir in speaker_dirs:            
            speaker_dir_path = os.path.join(output_path, speaker_dir)
            speaker_dir_path_output = os.path.join(output_path+"_chunks", speaker_dir) ## Temp directory for storing output
            alignment_cmd = "yes n | bin/mfa_align "+speaker_dir_path+ " librispeech-lexicon.txt english "+speaker_dir_path_output+" &"
            cmd_return = os.popen(alignment_cmd).readlines()
            os.system('pkill yes &') ## This ensures the 'yes' process terminates and doesnt keep running in the background
            copy_tree(speaker_dir_path_output, speaker_dir_path)  ## Copies the generated .TextGrid files alongside the .lab files in the input directory
            rmtree(Path(speaker_dir_path_output).parent)  ## Deletes the Temp direcotry created above
            parse_main(Path(speaker_dir_path).parent)  # Combine individual TextGrid files to generate alignment file
            rmtree(training_data_directory)
            copy_tree(Path(speaker_dir_path).parent, training_data_directory)
            rmtree(output_path)
        break ## This prevents the loop from processing the directories it just created, thereby avoiding an endless loop.
   print('Forced Alignment Complete!')
   
   for root, speaker_dirs, files in os.walk(training_data_directory):
       for speaker_dir in speaker_dirs:            
            speaker_dir_path = os.path.join(training_data_directory, speaker_dir)
            break
       break
   

   os.chdir(current_dir)
   print('------------------Stage 2 Complete-------------------')
   print('Run the following command to start fine-tuning the model on the pre-processed data:')
   print('python train_DeepTalk_step1.py ' + speaker_dir_path)
   print('-----------------------------------------------------')


if __name__ == "__main__":
   main(sys.argv[1:])
