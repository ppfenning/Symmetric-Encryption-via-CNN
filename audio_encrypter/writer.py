import numpy as np
import pandas as pd
from pathlib import Path
from scipy.io.wavfile import write
from conversion import bin_to_dec


def write_wav(rate: int, data: np.ndarray, outfile: Path):
    Path.mkdir(outfile.parent, exist_ok=True)
    return write(outfile, rate, data)


def binary_to_wav(rate: int, bdata: pd.Series, *, outfile: Path) -> (int, np.ndarray):
    dec_data = bin_to_dec(bdata)
    write_wav(rate, dec_data, outfile)
    return rate, dec_data
