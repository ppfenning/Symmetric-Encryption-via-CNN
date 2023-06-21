import numpy as np
from scipy.io.wavfile import read
import io
from pathlib import Path
from conversion import dec_to_bin
import pandas as pd


def read_wav(fname: Path) -> (int, np.ndarray):
    return read(io.BytesIO(fname.open('rb').read()))


def wav_to_binary(fname: Path) -> (int, pd.Series):
    rate, data = read_wav(fname)
    return rate, dec_to_bin(data)

