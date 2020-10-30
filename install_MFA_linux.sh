#!/bin/sh
wget https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner/releases/download/v1.0.1/montreal-forced-aligner_linux.tar.gz
tar -xvf montreal-forced-aligner_linux.tar.gz
rm -r montreal_forced_aligner_linux
mv montreal-forced-aligner montreal_forced_aligner_linux
rm montreal-forced-aligner_linux.tar.gz
cp montreal_forced_aligner_linux/lib/libpython3.6m.so.1.0 montreal_forced_aligner_linux/lib/libpython3.6m.so
cp montreal_forced_aligner_mac/librispeech-lexicon.txt montreal_forced_aligner_linux/



