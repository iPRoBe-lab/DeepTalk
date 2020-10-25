import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
from tqdm import tqdm
import librosa as lr
import fileinput

# importing libraries 
import speech_recognition as sr 
import soundfile as sf
import os 
from pathlib import Path
from pydub import AudioSegment 
from pydub.silence import split_on_silence 
from shutil import copyfile


# a function that splits the audio file into chunks 
# and applies speech recognition 
def silence_based_conversion(audio_path = "alice-medium.wav", output_dir = './chunks' , silence_length = 0.75): 

	# open the audio file stored in 
	# the local system as a wav file. 
    file_name = output_dir.split('/')[-1]

    song, sampling_rate = lr.load(audio_path, sr=16000)

	# split track where silence is 0.5 seconds 
	# or more and get chunks 
    chunks = lr.effects.split(y=song, frame_length=int(sampling_rate * silence_length), top_db=20)

    
	# move into the directory to 
	# store the audio files. 
    current_dir = os.getcwd()
    os.chdir(output_dir)
    r = sr.Recognizer() 

	# process each chunk 
    for i in tqdm(range(chunks.shape[0])): 
			
        audio_chunk = song[chunks[i,0]:chunks[i,1]]

        chunk_file_name = output_dir + '/' + file_name + '_' + str(i) + '.wav'
        chunk_test_file_name = output_dir + '/' + file_name + '_' + str(i) + '.lab'        
        sf.write(chunk_file_name, audio_chunk, sampling_rate, 'PCM_16')

        with sr.AudioFile(chunk_file_name) as source:
            audio = r.record(source)
            
        try: 
            trascript = r.recognize_google(audio)
            file1 = open(chunk_test_file_name, "w+")
            file1.write(trascript.upper())
            file1.close()
        
        except sr.UnknownValueError: 
            print("Speech Recognition could not understand audio")
            os.remove(chunk_file_name)
            print(chunk_file_name+" not written")
        
        except sr.RequestError as e: 
            print("Could not request results from Speech Recognition service; {0}".format(e)) 
    
    os.chdir(current_dir)

def split_audio_main(input_root_path, output_root_path):


    for root, speaker_dirs, files in os.walk(input_root_path):
        for speaker_dir in speaker_dirs:            
            speaker_dir_path = os.path.join(input_root_path,speaker_dir)
            for root, dirs, files in os.walk(speaker_dir_path):
                for filename in tqdm(files):
                    if os.path.splitext(filename)[1] == ".wav":
                        wav_path = os.path.join(speaker_dir_path,filename)
                        output_dir = str(Path(wav_path).parent).replace(input_root_path, output_root_path)
                        f_name = os.path.splitext(filename)[0]
                        output_dir = os.path.join(output_dir,f_name)                        
                        try: 
                            os.makedirs(output_dir)
                        except(FileExistsError): 
                            pass
                        
                        silence_based_conversion(wav_path,output_dir)



    
    
            
        
    
            


    
		
	 
