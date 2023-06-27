from pathlib import Path
from os import getenv
from encryption import get_encryption, get_key
from dotenv import load_dotenv
import numpy as np
from scipy.io.wavfile import read, write
import io

config = Path("../config/.env")

if config.exists():
    load_dotenv(config)


DATADIR = Path(getenv('DATADIR', default="../data"))
KEYPATH = Path(getenv('KEYPATH', default="~/.chaos-encrypt/private_key.pkl"))
OUTDIR = Path(getenv('OUTDIR', default=DATADIR.joinpath("out")))


def read_wav(fname: Path) -> (int, np.ndarray):
    return read(io.BytesIO(fname.open('rb').read()))


def write_wav(rate: int, data: np.ndarray, outfile: Path):
    Path.mkdir(outfile.parent, exist_ok=True)
    write(outfile, rate, data)
    return data


def audio_encrypter(in_file, outfile):

    throw_away = int(getenv('THROW_AWAY', default=np.random.randint(1000, 2000, 1)))

    rate, audio = read_wav(in_file)

    return write_wav(
        rate,
        get_encryption(audio, **get_key(KEYPATH, throw_away)),
        OUTDIR.joinpath(outfile)
    )


def get_speaker_file(speaker_id: int, section_no: int) -> Path:
    return DATADIR.joinpath('wav48', f"p{speaker_id}/p{speaker_id}_{section_no:03}.wav")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    val = audio_encrypter(OUTDIR.joinpath('encrypted.wav'), 'decrypted.wav')

