import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from audio_encrypter import read_wav
from acoustid import fingerprint_file


def get_fingerprints(*files):
    for file in files:
        yield fingerprint_file(file)


def __get_time_array(sample_rate: int, dlen: int) -> np.ndarray:
    return np.arange(0, dlen/sample_rate, 1/sample_rate)


def __get_axis_data(fname: Path) -> pd.DataFrame:
    rate, data = read_wav(fname)
    return pd.DataFrame({
        'Time[s]': __get_time_array(rate, len(data)),
        fname: data}
    ).set_index("Time[s]", drop=True)


def __get_file_df(*files) -> pd.DataFrame:
    for file in files:
        yield __get_axis_data(file)


def plot_wav(*files, figsize=(12, 8)):
    figs = get_file_amps(*files).plot(subplots=True, ylabel="Amplitude", figsize=figsize)
    plt.tight_layout()
    plt.show()
    return figs


def get_file_amps(*files) -> pd.DataFrame:
    return pd.concat(list(__get_file_df(*files)), axis=1)


def compare_files(file1: Path, file2: Path) -> pd.Series:
    df = get_file_amps(file1, file2)
    fprints = list(get_fingerprints(file1, file2))
    return pd.Series(
        [df[file1].equals(df[file2]), fprints[0] == fprints[1]],
        index=['checksum', 'fingerprints']
    )


