
##Parameters for Baseline

##Mel-filterbank
# mel_window_length = 25  # In milliseconds
# mel_window_step = 10    # In milliseconds
# mel_n_channels = 40
# # ## Audio for Mel-Spectrograms
# sampling_rate = 16000 # For mel-spectrograms
# # Number of spectrogram frames in a partial utterance
# partials_n_frames = 160     # 1600 ms
# # Number of spectrogram frames at inference
# inference_n_frames = 80     #  800 ms


##Parameters for fCNN

# # Mel-filterbank
mel_window_length = 25  # In milliseconds
mel_window_step = 10    # In milliseconds
mel_n_channels = 128
# Audio Parameters for fCNN
sampling_rate = 8000 # For mel-spectrograms
# Number of spectrogram frames in a partial utterance
partials_n_frames = 200     # 1600 ms
# Number of spectrogram frames at inference
inference_n_frames = 100     #  800 ms



## Voice Activation Detection
# Window size of the VAD. Must be either 10, 20 or 30 milliseconds.
# This sets the granularity of the VAD. Should not need to be changed.
vad_window_length = 30  # In milliseconds
# Number of frames to average together when performing the moving average smoothing.
# The larger this value, the larger the VAD variations must be to not get smoothed out.
vad_moving_average_width = 8
# Maximum number of consecutive silent frames a segment can have.
vad_max_silence_length = 6


## Audio volume normalization
audio_norm_target_dBFS = -30
