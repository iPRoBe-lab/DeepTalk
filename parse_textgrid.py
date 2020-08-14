import re, os
import textgrid
from pathlib import Path
from tqdm import tqdm

def process_textGrid(textGrid_path):

    utterance_id = Path(textGrid_path).name.strip()
    utterance_id = os.path.splitext(utterance_id)[0]

    tg = textgrid.TextGrid()
    tg.read(textGrid_path)
    words_tier = tg.tiers[0]
    mark_list = []
    maxTime_list = []


    for interval in words_tier.intervals:
        if (interval.mark != "<unk>"):
            mark_list.append(interval.mark.upper())
            maxTime_list.append(str(interval.maxTime))
    mark_string = ','.join(mark_list).strip()
    maxTime_string = ','.join(maxTime_list).strip()

    
    alignmentString = utterance_id + " \"" + mark_string + "\" \"" + maxTime_string + "\""
    transString = utterance_id + " " + ' '.join(mark_list).strip()
    return alignmentString, transString


def parse_main(text_grid_path):
    # text_grid_path = 'aligned_custom_data_chunks/'
    # output_path = 'custom_data_chunks/'

    speaker_dirs = next(os.walk(text_grid_path))[1] ## Get all speaker directories
    
    for speaker in tqdm(speaker_dirs):
        speaker_path = os.path.join(text_grid_path, speaker)
        sample_dirs = next(os.walk(speaker_path))[1]
        for sample_dir in tqdm(sample_dirs):
            sample_path = os.path.join(speaker_path,sample_dir)
            alignment_file = os.path.join(sample_path, sample_dir + '.alignment.txt')
            transcript_file = os.path.join(sample_path, sample_dir + '.trans.txt')

            f1 = open(alignment_file, 'w')
            f2 = open(transcript_file, 'w')
            

            for root, dirs, files in os.walk(sample_path):
                for filename in files:
                    if os.path.splitext(filename)[1] == ".TextGrid":
                        textGrid_path = os.path.join(sample_path,filename)
                        alignmentString, transString = process_textGrid(textGrid_path)
                        f1.write(alignmentString+'\n')  # python will convert \n to os.linesep
                        f2.write(transString+'\n')
            f1.close()
            f2.close()






    
    

