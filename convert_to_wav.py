import os
from pydub import AudioSegment
from tqdm import tqdm
import fileinput
mp3_path = '/scratch0/chowdh51/Data/LibriSpeech/train-other-WKAR/'

## Replace space in filenames with underscore
for root, dirs, files in os.walk(mp3_path):
    for filename in tqdm(files):
        if os.path.splitext(filename)[1] == ".wav" or os.path.splitext(filename)[1] == ".txt":
            os.rename(os.path.join(root, filename), os.path.join(root, filename.replace(' ', '_')))


## Convert .mp3 to .wav
def mp3gen():
    for root, dirs, files in os.walk(mp3_path):
        for filename in files:
            if os.path.splitext(filename)[1] == ".mp3":
                yield os.path.join(root, filename)

for mp3file in tqdm(mp3gen()):
    dst = mp3file.replace('.mp3', '.wav')
    # convert wav to mp3                                                            
    sound = AudioSegment.from_mp3(mp3file)
    sound = sound.set_frame_rate(16000)
    sound.export(dst, format="wav")
    os.remove(mp3file)
    
# /scratch0/chowdh51/Data/LibriSpeech/train-other-WKAR/Brad/20200527_Brad_confrontation_in_north_Lansing.txt
# /scratch0/chowdh51/Data/LibriSpeech/train-other-WKAR/Brad/20200527_Brad_confrontation_in_north_Lansing.wav