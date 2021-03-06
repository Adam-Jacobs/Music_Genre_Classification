import tqdm
import warnings

# Feature extraction imports
import librosa
import numpy as np

# Concurrency imports
from multiprocessing import Pool
from multiprocessing import Queue
from time import sleep
import gc

# File path retrieval imports
import os
import sys
from common import file_utils as utils


def extract_features(track_path, include_path=False):
    features = []
    y, sr = librosa.load(track_path)

    # Track Title
    if include_path:
        features.append(os.path.splitext(os.path.basename(track_path))[0])

    # Zero Crossing Rate
    zcr = librosa.feature.zero_crossing_rate(y)
    features.append(zcr.sum() / zcr.size)

    # Mel Frequency Cepstral Coefficient
    mfccs = librosa.feature.mfcc(y=y, sr=sr)
    for i in range(0, 20):
        features.append(mfccs[i].sum() / mfccs[i].size)

    # Spectral Centroid
    cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    features.append(cent[0].sum() / cent[0].size)

    gc.collect()

    return features


def extract_featrues_directory(dir_path, resume=False):
    track_paths = utils.get_files(dir_path, '.mp3')

    if resume:
        resume_interval = 100
    else:
        resume_interval = len(track_paths + 1)  # need to check  if this works

    for i in range(len(os.listdir("data")) * resume_interval, len(track_paths), resume_interval):
        tracks = []

        with Pool(os.cpu_count() - 2) as pool:
            tracks.extend(tqdm.tqdm(pool.imap(extract_features, track_paths[i:i+resume_interval]), total=resume_interval))

        gc.collect()

        np.savetxt("data\\features" + str(int(i / resume_interval)) + ".csv", tracks, delimiter=",", fmt="%s")
