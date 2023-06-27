from pathlib import Path
from os import getenv
from .encryption import get_encryption, get_key
import numpy as np
from scipy.io.wavfile import read, write
import io


def read_wav(fname: Path) -> (int, np.ndarray):
    return read(io.BytesIO(fname.open('rb').read()))


def write_wav(rate: int, data: np.ndarray, outfile: Path):
    Path.mkdir(outfile.parent, exist_ok=True)
    write(outfile, rate, data)
    return data


def audio_encrypter(in_file: Path, outfile: Path, keypath: Path) -> [int, np.ndarray]:

    throw_away = int(getenv('THROW_AWAY', default=np.random.randint(1000, 2000, 1)))
    rate, audio = read_wav(in_file)

    return rate, audio, write_wav(
        rate,
        get_encryption(audio, **get_key(keypath, throw_away)),
        outfile
    )

