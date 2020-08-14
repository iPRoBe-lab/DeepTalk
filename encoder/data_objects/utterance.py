import numpy as np
from scipy import stats

class Utterance:
    def __init__(self, frames_fpath, wave_fpath):
        self.frames_fpath = frames_fpath
        self.wave_fpath = wave_fpath

    def get_frames(self):
        frames = np.load(self.frames_fpath)
        if(frames.shape[1]==160):  ## Zscore normalize raw audio frame
            frames = stats.zscore(frames, axis=1, ddof=1)
            
        return frames

    def random_partial(self, n_frames):
        """
        Crops the frames into a partial utterance of n_frames

        :param n_frames: The number of frames of the partial utterance
        :return: the partial utterance frames and a tuple indicating the start and end of the
        partial utterance in the complete utterance.
        """

        frames = self.get_frames()

        ## Make sure the data is of minimum length "windows_size"
        if (frames.shape[0]-n_frames < 0):
            factor = int(np.ceil(n_frames/frames.shape[0]))
            frames = np.tile(frames,(factor+1,1))

        if frames.shape[0] == n_frames:
            start = 0
        else:
            start = np.random.randint(0, frames.shape[0] - n_frames)
        end = start + n_frames
        return frames[start:end], (start, end)
