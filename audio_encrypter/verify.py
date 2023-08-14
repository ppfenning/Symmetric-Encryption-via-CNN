import numpy as np
from scipy.stats import entropy
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from audio_encrypter.chaotic_audio_encryption import read_wav, chaotic_ciphertext, write_wav
from acoustid import fingerprint_file
from time import time


def get_fingerprints(*files):
    for file in files:
        yield fingerprint_file(file)


def __get_time_array(sample_rate: int, dlen: int) -> np.ndarray:
    """
    The __get_time_array function takes in a sample rate and data length,
    and returns an array of time values that correspond to the data.
    The function is used by the __get_fft_data function.

    :param sample_rate: int: Set the sample rate of the data
    :param dlen: int: Determine the length of the sound array
    :return: An array of time values
    :doc-author: Trelent
    """
    return np.arange(0, dlen/sample_rate, 1/sample_rate)


def __get_axis_data(fname: Path) -> pd.DataFrame:
    """
    The __get_axis_data function takes a file path and returns a pandas DataFrame with the following columns:
        - Time[s]: The time in seconds of each sample.
        - fname: The data from the wav file at that time.

    :param fname: Path: Specify the file name of the wav file
    :return: A dataframe with the time axis and the sound data
    :doc-author: Trelent
    """
    rate, data = read_wav(fname)
    index = __get_time_array(rate, data.shape[0])
    return pd.DataFrame(data, index=index, columns=[f"CHANNEL_{i}" for i in range(data.ndim)])


def __get_file_df(*files) -> pd.DataFrame:
    """
    The __get_file_df function takes in a variable number of files and returns a generator object that yields
    a pandas DataFrame for each file. The __get_axis_data function is called on each file to get the data from the
    file, which is then returned as a DataFrame.

    :param *files: Pass in any number of files to the function
    :return: A generator object
    :doc-author: Trelent
    """
    for file in files:
        yield __get_axis_data(file)


def wav_entropy(wav, base=None):
  value,counts = np.unique(wav, return_counts=True)
  return entropy(counts, base=base)


def PSNR(original, encrypted):
    original = original/original.max(axis=0)*255
    encrypted = encrypted/encrypted.max(axis=0)*255
    diff = original - encrypted
    mse = np.power(diff, 2).mean()
    if mse == 0:  # MSE is zero means no noise is present in the signal .
        # Therefore PSNR have no importance.
        return 100
    max_amp = 255.
    psnr = 20 * np.log10(max_amp / np.sqrt(mse))
    return psnr


def plot_wav(*dfs, figsize: tuple = (12, 8)):
    """
    The plot_wav function takes in a list of files and plots the amplitude of each file.

    :param *files: Pass in a variable number of files
    :param figsize: Set the size of the figure
    :return: A tuple of matplotlib
    :doc-author: Trelent
    """
    def plotter(df):
        figs = df.plot(subplots=True, ylabel="Amplitude", figsize=figsize)
        plt.tight_layout()
        plt.show()
        return figs

    return list(map(plotter, *dfs))


def get_file_amps(*files) -> list:
    """
    The get_file_amps function takes a list of files and returns a dataframe with the amplitudes for each file.

    :param *files: Accept multiple arguments
    :return: A dataframe with the amplitude values of each file
    :doc-author: Trelent
    """
    return list(__get_file_df(*files))


def all_equal(dfs):
    return all(list(map(lambda other: dfs[0].equals(other), dfs[1:])))


def compare_files(*files) -> [bool, list[pd.DataFrame]]:
    """
    The compare_files function takes two file paths as input and returns a pandas Series object
    with the following information:
        - checksum: whether the files have identical amplitudes (True/False)
        - fingerprints: whether the files have identical fingerprints (True/False)

    :param file1: Path: Specify the first file to compare
    :param file2: Path: Specify the second file that is being compared to the first
    :return: A pd
    :doc-author: Trelent
    """
    amps = get_file_amps(*files)
    check = all_equal(amps)
    return check, pd.concat(amps, axis=1)


def avg_chaotic_audio_encryption_time(
    in_file: Path,
    outfile: Path,
    keypath: Path,
    nruns: int | None = None
) -> dict:
    """
    The chaotic_audio_encryption function takes in a .wav file, encrypts it using the chaotic_ciphertext function,
    and writes the encrypted audio to an output file. The keypath argument is used to specify where the key should be
    stored.

    :param in_file: Path: Specify the file path of the audio file to be encrypted
    :param outfile: Path: Specify the name of the output file
    :param keypath: Path: Specify the path to the key file
    :return: The sample rate and the encrypted audio
    :doc-author: Trelent
    """
    if not nruns:
        nruns = 5
    print("*"*100)
    print(f"Encrypting {in_file}:")
    print("="*100)
    print(f"Iterations: {nruns}")
    print(f"File size: {in_file.lstat().st_size/(1024**2):.2f} MB")
    rate, audio = read_wav(in_file)
    print(f"Channels: {audio.ndim}")
    print("-"*100)
    size = in_file.lstat().st_size / (1024 ** 2)
    t1 = time()
    for _ in range(nruns):
        encrypted = chaotic_ciphertext(audio, keypath)
    t2 = time()
    avg_time = (t2-t1)/nruns
    print(f"Average encryption time: {avg_time:.5f} seconds")
    write_wav(rate, encrypted, outfile)
    print(f"Encrypted path: {outfile}")
    return {
        "size": size,
        "encryption_time": avg_time,
        "channels": audio.ndim
    }


def run_folder_stats(in_folder, out_folder, prefix, keypath, nruns=None):
    stats = dict()
    for in_file in in_folder.iterdir():
        out_file = out_folder.joinpath(f"{prefix}{in_file.name}")
        stats[in_file.name] = avg_chaotic_audio_encryption_time(in_file, out_file, keypath, nruns)
    return pd.DataFrame(stats).T.sort_values("size")
