from pathlib import Path
from chaotic_encrypter.encryption import chaotic_ciphertext
import numpy as np
from scipy.io.wavfile import read, write
import io


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
    return rate, data


def chaotic_audio_encryption(
    in_file: Path,
    out_file: Path,
    key_path: Path,
) -> tuple[int, np.ndarray]:
    rate, audio = read_wav(in_file)
    cipher_text = chaotic_ciphertext(audio, key_path)
    write_wav(rate, cipher_text, out_file)
    return rate, cipher_text
