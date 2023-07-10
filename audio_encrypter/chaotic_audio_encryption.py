from pathlib import Path
from .encryption import chaotic_ciphertext
import numpy as np
from scipy.io.wavfile import read, write
import io


def read_wav(fname: Path) -> (int, np.ndarray):
    return read(io.BytesIO(fname.open('rb').read()))


def write_wav(rate: int, data: np.ndarray, outfile: Path) -> np.ndarray:
    Path.mkdir(outfile.parent, exist_ok=True)
    write(outfile, rate, data)
    return data


def chaotic_audio_encryption(in_file: Path, outfile: Path, keypath: Path) -> [int, np.ndarray]:
    rate, audio = read_wav(in_file)
    return write_wav(rate, chaotic_ciphertext(audio, keypath), outfile)

