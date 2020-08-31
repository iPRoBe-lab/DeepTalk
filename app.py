import os
from flask import Flask, request, render_template, flash, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
# from commons import get_tensor
# from inference import get_speaker_embedding
from os import walk, listdir, path
from os.path import isfile, join
from demo_functions import run_DeepTalk_demo as DeepTalk
import soundfile as sf
from pathlib import Path
from encoder import audio
import librosa as lr
import numpy as np


os.environ["CUDA_VISIBLE_DEVICES"] = '0,1'

UPLOAD_FOLDER = 'uploads'
MODEL_FOLDER = 'trained_models'
NOISE_FOLDER = 'uploads/Noise'
NOISE_FILE = 'uploads/Noise/Babble.wav'
GENERATED_AUDIO_FILE = 'uploads/ref_gen.wav'
MODIFIED_AUDIO_FILE = 'uploads/ref_gen_modified.wav'
REF_MELSPEC_IMG = 'uploads/ref_melspec.png'
SYN_MELSPEC_IMG = 'uploads/syn_melspec.png'
TARGET_TEXT_FILE = 'target_text_dir/target_text.txt'
ALLOWED_EXTENSIONS = {'.wav', '.WAV', '.mp3', '.m4a'}
ENC_MODULE_NAME = "model_GST"

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['NOISE_FOLDER'] = NOISE_FOLDER
app.config['NOISE_FILE'] = NOISE_FILE
app.config['MODEL_FOLDER'] = MODEL_FOLDER
app.config['ENC_MODULE_NAME'] = ENC_MODULE_NAME
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # will limit the maximum allowed payload to 16 megabytes.
app.config['TARGET_TEXT_FILE'] = TARGET_TEXT_FILE
app.config['GENERATED_AUDIO_FILE'] = GENERATED_AUDIO_FILE
app.config['MODIFIED_AUDIO_FILE'] = MODIFIED_AUDIO_FILE
app.config['REF_MELSPEC_IMG'] = REF_MELSPEC_IMG
app.config['SYN_MELSPEC_IMG'] = SYN_MELSPEC_IMG
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_COOKIE_SECURE'] = True
# uploaded_files = [f for f in listdir(app.config['UPLOAD_FOLDER']) if isfile(join(app.config['UPLOAD_FOLDER'], f))]
# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        # (_, _, uploaded_files) = next(walk(app.config['UPLOAD_FOLDER']))
        (_, uploaded_files, _) = next(walk(app.config['MODEL_FOLDER']))
        
        with open(app.config['TARGET_TEXT_FILE'], 'r') as file:
            target_text = file.read()
        return render_template('index.html', uploaded_files=uploaded_files, upload_folder = app.config['UPLOAD_FOLDER'], model_folder = app.config['MODEL_FOLDER'], target_text = target_text, synthetic_audio = "",
            ref_melspec_img = app.config['REF_MELSPEC_IMG'], syn_melspec_img = app.config['SYN_MELSPEC_IMG'])

    if request.method == 'POST':

        print(request.form)

        if 'target_text_form6' in request.form:
            gen_audio, sr1 = lr.load(app.config['GENERATED_AUDIO_FILE'], sr=16000)            
            noise_audio, sr2 = lr.load(app.config['NOISE_FILE'], sr=16000)            
            lspeed = float(request.form['speed'])
            lpitch = float(request.form['pitch'])
            lnoise = float(request.form['noise'])

            noise_audio = np.resize(noise_audio, len(gen_audio))
            
            modified_audio = gen_audio
            if (lspeed != 1):
                modified_audio = lr.effects.time_stretch(modified_audio, lspeed)
            if (lpitch != 0):    
                modified_audio = lr.effects.pitch_shift(modified_audio, sr1, n_steps=lpitch)
            if (lnoise != 0):    
                modified_audio = modified_audio + lnoise*noise_audio

            sf.write(app.config['MODIFIED_AUDIO_FILE'], modified_audio, sr1, 'PCM_24')
     
        
        if 'target_text_form2' in request.form:
            # (_, _, uploaded_files) = next(walk(app.config['UPLOAD_FOLDER']))
            (_, uploaded_files, _) = next(walk(app.config['MODEL_FOLDER']))
            with open(app.config['TARGET_TEXT_FILE'], 'r') as file:
                target_text = file.read()
            ref_audio_path = request.form['target_text_form2']
            enc_model_fpath = Path(request.form['target_text_form3'])
            enc_module_name = app.config['ENC_MODULE_NAME']
            syn_model_dir = Path(request.form['target_text_form4'])
            voc_model_fpath = Path(request.form['target_text_form5'])

            

            synthesized_wav, sample_rate, _ = DeepTalk(ref_audio_path=ref_audio_path, output_text=target_text,
            enc_model_fpath=enc_model_fpath, enc_module_name=enc_module_name,
            syn_model_dir=syn_model_dir, voc_model_fpath=voc_model_fpath)

            sf.write(app.config['GENERATED_AUDIO_FILE'], synthesized_wav, sample_rate, 'PCM_24')


            if(path.exists(app.config['GENERATED_AUDIO_FILE'])):
                flash('Synthetic Audio Generated!!')

            return render_template('index.html', uploaded_files=uploaded_files, upload_folder=app.config['UPLOAD_FOLDER'], model_folder=app.config['MODEL_FOLDER'], target_text=target_text, synthetic_audio=app.config['GENERATED_AUDIO_FILE'], syn_melspec_img = app.config['SYN_MELSPEC_IMG'])


        if 'target_text_form' in request.form:
            target_text = request.form['target_text_form']
            file1 = open(app.config['TARGET_TEXT_FILE'],"w")
            file1.writelines(target_text)
            file1.close() #to change file access modes
            flash('Target text updated!!')
            (_, uploaded_files, _) = next(walk(app.config['MODEL_FOLDER']))
            with open(app.config['TARGET_TEXT_FILE'], 'r') as file:
                target_text = file.read()
            return render_template('index.html', uploaded_files=uploaded_files, upload_folder=app.config['UPLOAD_FOLDER'], model_folder=app.config['MODEL_FOLDER'], target_text=target_text, synthetic_audio="", syn_melspec_img = app.config['SYN_MELSPEC_IMG'])

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('Invalid file selected')
            (_, uploaded_files, _) = next(walk(app.config['MODEL_FOLDER']))
            with open(app.config['TARGET_TEXT_FILE'], 'r') as file:
                target_text = file.read()
            return render_template('index.html', uploaded_files=uploaded_files, upload_folder = app.config['UPLOAD_FOLDER'], model_folder = app.config['MODEL_FOLDER'], target_text = target_text, synthetic_audio = "", syn_melspec_img = app.config['SYN_MELSPEC_IMG'])

        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file:
        # if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            (_, uploaded_files, _) = next(walk(app.config['MODEL_FOLDER']))
            with open(app.config['TARGET_TEXT_FILE'], 'r') as file:
                target_text = file.read()
            return render_template('index.html', uploaded_files=uploaded_files, upload_folder = app.config['UPLOAD_FOLDER'], model_folder = app.config['MODEL_FOLDER'], target_text = target_text, synthetic_audio = None, syn_melspec_img = app.config['SYN_MELSPEC_IMG'])

    return

# No caching at all for API endpoints.
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

if __name__ == '__main__':
	app.run(debug=True)

## REMEMBER  to not use development environment in production code
# How to run this in development mode:
# export FLASK_ENV=development
# export FLASK_APP=app.py
# flask run
