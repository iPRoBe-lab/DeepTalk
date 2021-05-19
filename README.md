DeepTalk
===============================

PyTorch implementation of the DeepTalk model described in *DeepTalk: Vocal Style Encoding for Speaker Recognition and Speech Synthesis* by A. Chowdhury, A. Ross, and P. David in IEEE International Conference on Acoustics, Speech and Signal Processing 2021 (ICASSP-2021).

## Research Article

[Anurag Chowdhury](https://github.com/ChowdhuryAnurag), [Arun Ross](http://www.cse.msu.edu/~rossarun/), and [Prabu David](https://comartsci.msu.edu/our-people/prabu-david), *DeepTalk: Vocal Style Encoding for Speaker Recognition and Speech Synthesis*, IEEE International Conference on Acoustics, Speech and Signal Processing (2021).  

- arXiv: [https://arxiv.org/abs/2012.05084](https://arxiv.org/abs/2012.05084)

## Description

DeepTalk is a deep-learning based vocal style transfer model developed by A. Chowdhury, A. Ross, and P. David, at Michigan State University.
The model requires a reference audio from a target speaker and a sample text to synthesize speech audio that mimics the vocal identity of the target speaker uttering the sample text. 

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
    Type [y] when prompted to Proceed([y]/n)
    
    1.3) Activate the deeptalk python environment
    ```
    conda activate deeptalk
    ```

2) Additional requirements are listed in the [./requirements.txt](./requirements.txt) file. Install them as follows:
    ```
    pip install -r requirements.txt
    ```

3) Now, we need to install [Montreal-Forced-Aligner](https://montreal-forced-aligner.readthedocs.io/en/latest/). For this project it could be done in the following two ways:

    3.1) Download and install the Montreal-Forced-Aligner following the instructions [here](https://montreal-forced-aligner.readthedocs.io/en/latest/installation.html). We have included a copy of Montreal-Forced-Aligner (both for Linux and Mac OS) with this repository to serve as a template for the directory structure expected by the DeepTalk implementation. Please note that the *librispeech-lexicon.txt* file included in both the montreal_forced_aligned_mac and montreal_forced_aligned_linux are important for this project and should be retained in this final installation of Montreal-Forced-Aligner.
    
    3.2) Alternatively, you can also run the [install_MFA_linux.sh](./install_MFA_linux.sh) script (only works for Linux machines) to automatically download and install Montreal-Forced-Aligner. This script also fixes some of the most common installation [issues](https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner/issues/109) associated with running Montreal-Forced-Aligner on linux machines.
    ```
    ./install_MFA_linux.sh
    ```

    3.3) Now, run the following command to ensure Montreal-Forced-Aligner was installed correctly and is working fine.
    ```
    montreal_forced_aligner_linux/bin/mfa_align
    ```
    You should get the following output if everything is working fine:
    ```
    usage: mfa_align [-h] [-s SPEAKER_CHARACTERS] [-b BEAM] [-t TEMP_DIRECTORY]
                    [-j NUM_JOBS] [-v] [-n] [-c] [-d] [-e] [-i] [-q]
                    corpus_directory dictionary_path acoustic_model_path
                    output_directory
    mfa_align: error: the following arguments are required: corpus_directory, dictionary_path, acoustic_model_path, output_directory
    ```

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

1) The DeepTalk model can be finetuned to mimic the voice of a target speaker of your choice. For this process, you will need to place high quality audio wave files containing speech from the target speaker in *Data/SampleAudio directory* as follows:
```
Data/SampleAudio/<speaker_name>/<fileid_subjectname_audiotitle.wav>
```
Example:
```
Data/SampleAudio/Speaker1/1_Speaker1_BroadcastIndustry.wav
```
We have included few sample audios (through the *trained_model.zip*) following the directory format specified above, to serve as a reference. These sample audios can be listed using the following command:
```
ls Data/SampleAudio/Speaker1/
```

3) Run *preprocess_audio.py <input_directory> <output_directory>* to preprocess the audio from previous step to make it compatible for fine-tuning the DeepTalk model.
```
python preprocess_audio.py Data/SampleAudio Data/ProcessedAudio
```
The processed audio will be saved at *Data/LibriSpeech/train-other-custom/<speaker_name>*

4) Run *train_DeepTalk_step1.py <preprocessed_audio_directory>* to use the preprocessed audio to fine-tune the Synthesizer of the DeepTalk model.
```
python train_DeepTalk_step1.py Data/LibriSpeech/train-other-custom/Speaker1
```

5) Run *train_DeepTalk_step2.py <preprocessed_audio_directory>* to use the preprocessed audio to fine-tune the Vocoder of the DeepTalk model.
```
python train_DeepTalk_step2.py Data/LibriSpeech/train-other-custom/Speaker1
```

6) A fine-tuned model directory bearing the <speaker_name> should now appear in the trained_models directory


**Acknowledgement**

Portions of this implementation are based on [this](https://github.com/CorentinJ/Real-Time-Voice-Cloning) repository.

## Citation
If you use this repository then please cite:

```bibtex
@InProceedings{chowdhDeepTalk21,
  author       = "Chowdhury, A. and Ross, A. and David, P.",
  title        = "DeepTalk: Vocal Style Encoding for Speaker Recognition and Speech Synthesis",
  booktitle    = "ICASSP",
  year         = "2021",
}
```
