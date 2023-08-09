from pathlib import Path
from audio_encrypter.encryption import chaotic_ciphertext
import numpy as np
from scipy.io.wavfile import read, write
import io
from time import time


def read_wav(fname: Path) -> (int, np.ndarray):
    """
    The read_wav function reads a .wav file and returns the sampling rate (in samples/sec) and data from the file.

    :param fname: Path: Specify the file name
    :return: A tuple of two elements:
    :doc-author: Trelent
    """
    return read(io.BytesIO(fname.open('rb').read()))


def write_wav(rate: int, data: np.ndarray, outfile: Path) -> tuple[int, np.ndarray]:
    """
    The write_wav function takes a sampling rate, an array of data, and an output file path.
    It creates the directory for the output file if it doesn't exist already.
    Then it writes the data to a wav file at that location.

    :param rate: int: Set the sampling rate of the audio file
    :param data: np.ndarray: Specify the data to be written
    :param outfile: Path: Specify the file path of the output file
    :return: The data array
    :doc-author: Trelent
    """
    Path.mkdir(outfile.parent, exist_ok=True)
    write(outfile, rate, data)


def chaotic_audio_encryption(
    in_file: Path,
    outfile: Path,
    keypath: Path,
    nruns: int = 1
) -> tuple[int, np.ndarray, float]:
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
    print("*"*100)
    print(f"Encrypting {in_file}:")
    print("="*100)
    print(f"Iterations: {nruns}")
    print(f"File size: {in_file.lstat().st_size/(1024**2)} MB")
    rate, audio = read_wav(in_file)
    print(f"Channels: {audio.ndim}")
    print("-"*100)
    total_time = 0
    for _ in range(nruns):
        t1 = time()
        cipher_text = chaotic_ciphertext(audio, keypath)
        t2 = time()
        total_time += t2 - t1
    avg_time = total_time / nruns
    write_wav(rate, cipher_text, outfile)
    print(f"Average encryption time: {avg_time} seconds")
    print(f"Encrypted path: {outfile}")
    return rate, cipher_text, avg_time

