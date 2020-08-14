import os
from tqdm import tqdm
import fileinput

from num2words import num2words
mp3_path = '/scratch0/chowdh51/Data/LibriSpeech/train-other-WKAR/'

from nltk.tokenize import word_tokenize
## Remove empty lines from txt files
def remove_empty_lines(filename):
    if not os.path.isfile(filename):
        print("{} does not exist ".format(filename))
        return
    with open(filename) as filehandle:
        lines = filehandle.readlines()

    with open(filename, 'w') as filehandle:
        lines = filter(lambda x: x.strip(), lines)
        lines = lines.replace('\n', ' ').replace('\r', '')
        filehandle.writelines(lines.upper())
        
# Remove empty lines from txt files
for root, dirs, files in os.walk(mp3_path):
    for filename in tqdm(files):
        if os.path.splitext(filename)[1] == ".txt":
            dst = filename.replace('.txt', '.lab')
            file1 = open(os.path.join(root, filename), "r")
            file_text = file1.read()
            file1.close()
            # split into words
            tokens = word_tokenize(file_text)
            # remove all tokens that are not alphabetic
            words = []

            for word in tokens:
                if word.isalpha():
                    words.append(word.upper())
                elif word.isnumeric():
                    words.append(num2words(word).upper())

            file2 = open(os.path.join(root, dst), "w")

            for word in words:
                file2.write("%s " % word)
            file2.close()


