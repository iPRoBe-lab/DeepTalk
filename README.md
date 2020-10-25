
DeepTalk
===============================

DeepTalk is a deep-learning based vocal style transfer model developed by A. Chowdhury, A. Ross, and P. David, at Michigan State University.
The model requires a <reference audio> from a <target speaker> and a <sample text> to synthesis speech audio that mimics the vocal identity of the <target speaker> uttering the <sample text>. 

![DeepTalk Model](/images/DeepTalk.png)


## Implementation details and requirements

1) The model was implemented in PyTorch 1.3.1 and tensorflow 1.14 using Python 3.7 and may be compatible with different versions of PyTorch, tensorflow, and Python, but it has not been tested.

2) Additional requirements are listed in the [./requirements.txt](./requirements.txt) file. 

3) Run pip install requirements.txt to install the dependencies:
(The GPU versions of pytorch and tensorflow is recommended for faster training and inference)

4) We have included a copy of Montreal-Forced-Aligner (both for Linux and Mac OS) with this repository. However, it is highly recommended to replace them with their latest versions from
[Montreal-Forced-Aligner](https://montreal-forced-aligner.readthedocs.io/en/latest/installation.html#linux)

## Usage

**Pre-trained DeepTalk Model**

1) Please contact the maintainer of this repository at [chowdh51@msu.edu] for access to the pretrained DeepTalk models.
2) The pre-trained models for the DeepTalk Encoder, Synthesizer, and Vocoder should be placed in [./trained_models/Generic](./trained_models/Generic)
3) These models are trained on the [LibriSpeech](http://www.openslr.org/resources/12/train-other-500.tar.gz) and [VoxCeleb 1 and 2](http://www.robots.ox.ac.uk/~vgg/data/voxceleb/) datasets.
4) The pre-trained models are primarily used as a starting point for fine-tuning with speech data from a target speaker.

**Finetuning the DeepTalk model for a target speaker**

1) Place an audio wave file for fine-tuning the pre-trained DeepTalk Model in Data/SampleAudio directory as follows:
```
Data/SampleAudio/<speaker_name>/<fileid_subjectname_audiotitle.wav>
```
Example:
```
Data/SampleAudio/Vincent/1_Vincent_BedtimeStories.wav
```
We have already created the Data/SampleAudio directory with an audio from a speaker to serve as an example.

2) Run [Python preprocess_audio.py <input_directory> <output_directory>](This will preprocess the audio from previous step to make it compatible for fine-tuning the DeepTalk model)
Example: 
```
Python preprocess_audio.py Data/SampleAudio Data/ProcessedAudio
```

3) Run train_DeepTalk_step1.py (This will use the preprocessed audio to fine-tune the DeepTalk model)

4) A fine-tuned model directory bearing the <speaker_name> should now appear in the trained_models directory

