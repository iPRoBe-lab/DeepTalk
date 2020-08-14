1)Run pip install requirements.txt to install the dependencies:
(The GPU versions of pytorch and tensorflow is recommended for faster training and inference)

2) Place an audio wave file for fine-tuning the system in Data/SampleAudio directory.


1) Create an audio directory (named SampleAudio) in Data with the following structure:
    >Data
    >>SampleAudio
    >>>speaker_name
    >>>>fileid_subjectname_audiotitle.wav [PCM16 encoded]
    Ensure there are no spaces in fileid, subjectname, or audiotitle

   We have already created the Data/SampleAudio directory with an audio from a speaker to serve as an example.

2) run preprocess_audio.py (This will preprocess the audio from previous step to make it compatible for fine-tuning the DeepTalk model)
Example: python preprocess_audio.py Data/SampleAudio Data/ProcessedAudio

3) run train_DeepTalk.py (This will use the preprocessed audio to fine-tune the DeepTalk model)

4) A fine-tuned model directory bearing the <speaker_name> should now appear in the trained_models directory

