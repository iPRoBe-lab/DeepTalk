DeepTalk
===============================

DeepTalk is a deep-learning based vocal style transfer model developed by A. Chowdhury, A. Ross, and P. David, at Michigan State University.
The model requires a <reference audio> from a <target speaker> and a <sample text> to synthesis speech audio that mimics the vocal identity of the <target speaker> uttering the <sample text>. 

![DeepTalk Model](/images/DeepTalk.png)


**Downloading the DeepTalk code**

1) Clone the git repository

```
git clone git@github.com:ChowdhuryAnurag/DeepTalk-Deployment.git
```

2) Now you should have a folder named 'DeepTalk-Deployment'

3) Go into the folder 'DeepTalk-Deployment'
```
cd DeepTalk-Deployment
```

4) Please contact the maintainer of this repository at [chowdh51@msu.edu] for access to the pretrained DeepTalk models. Unzip 'trained_models.zip' (received separately from the maintainer) into this folder
```
unzip trained_models.zip
```

5) Now you should have a folder named 'trained_models' with several pretrained models in it

6) The Generic model is primarily used as a starting point for fine-tuning with speech data from a target speaker. The other models (Hannah, Ted, and Gordon Smith) are some sample finetuned models based on speech data from internal sources.

7) The Generic model is trained on the [LibriSpeech](http://www.openslr.org/resources/12/train-other-500.tar.gz) and [VoxCeleb 1 and 2](http://www.robots.ox.ac.uk/~vgg/data/voxceleb/) datasets.


**Setting up the python environment for running the DeepTalk code**

1) The model was implemented in PyTorch 1.3.1 and tensorflow 1.14 using Python 3.6.8 and may be compatible with different versions of PyTorch, tensorflow, and Python, but it has not been tested. (The GPU versions of pytorch and tensorflow is recommended for faster training and inference)

1.1) Install anaconda python distribution from https://www.anaconda.com/products/individual

1.2) Create an anaconda environment called 'deeptalk'
```
conda create -n deeptalk python=3.6.8
```
```
Type [y] when prompted to Proceed([y]/n)
```
1.3) Activate the deeptalk python environment
```
conda activate deeptalk
```

2) Additional requirements are listed in the [./requirements.txt](./requirements.txt) file. Install them as follows:
```
pip install -r requirements.txt
```

7) We have included a copy of Montreal-Forced-Aligner (both for Linux and Mac OS) with this repository. However, it is highly recommended to replace them with their latest release from
[Montreal-Forced-Aligner](https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner/releases/).

Please note: Montreal-Forced-Aligner sometimes fails to run after installation. Please refer [here](https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner/issues/109) for some of the most common issues faced by us and their possible solutions.

**Running the DeepTalk GUI to generate synthetic audio using pre-trained models received from the code maintainer**

Note: You should already be inside 'DeepTalk-Deployment' directory with 'deeptalk' conda environment activated.

1) Execute the following two commands to run the GUI prototype
```
export FLASK_APP=app.py
flask run
```

You should now be able to access the GUI prototype in your web browser at the below URL:
```
http://localhost:5000/
```


**Finetuning the DeepTalk model for a target speaker**

1) Create the Data/SampleAudio directory in the 'DeepTalk-Deployment' directory, as follows:
```
mkdir Data
mkdir Data/SampleAudio
```

2) Place an audio wave file for fine-tuning the pre-trained DeepTalk Model in Data/SampleAudio directory as follows:
```
Data/SampleAudio/<speaker_name>/<fileid_subjectname_audiotitle.wav>
```
Example:
```
Data/SampleAudio/Speaker1/1_Speaker1_BroadcastIndustry.wav
```

3) Run [Python preprocess_audio.py <input_directory> <output_directory>](This will preprocess the audio from previous step to make it compatible for fine-tuning the DeepTalk model)
Example: 
```
python preprocess_audio.py Data/SampleAudio Data/ProcessedAudio
```
The processed audio will be saved at Data/LibriSpeech/train-other-custom/<speaker_name>

4) Run train_DeepTalk_step1.py <preprocessed_audio_directory> (This will use the preprocessed audio to fine-tune the Synthesizer of the DeepTalk model)
```
python train_DeepTalk_step1.py Data/LibriSpeech/train-other-custom/Speaker1
```

5) Run train_DeepTalk_step2.py <preprocessed_audio_directory> (This will use the preprocessed audio to fine-tune the Vocoder of the DeepTalk model)
```
python train_DeepTalk_step2.py Data/LibriSpeech/train-other-custom/Speaker1
```

6) A fine-tuned model directory bearing the <speaker_name> should now appear in the trained_models directory
