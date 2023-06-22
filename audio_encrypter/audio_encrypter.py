from pathlib import Path
import numpy as np
from os import getenv
from reader import read_wav
from encryption import get_encryption
from conversion import dec_to_bin
from dotenv import load_dotenv

configdir = Path("../config")
env_file = configdir.joinpath(".env")

if env_file.exists():
    load_dotenv(env_file)


datadir = Path(getenv('DATADIR', default="../data"))
wavedir = datadir.joinpath('wav48')
outdir = Path(getenv('OUTDIR', default=datadir.joinpath("out")))


def get_speaker_file(speaker_id: int, section_no: int) -> Path:
    return wavedir.joinpath(f"p{speaker_id}/p{speaker_id}_{section_no:03}.wav")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    audio = dec_to_bin(read_wav(get_speaker_file(340, 340))[1])

    encryption_key = {
        'throw_away': 1000,
        'henon_0': np.random.random(2),
        'ikeda_0': np.random.random(2),
        'lorenz_0': np.random.random(3),
        'logistic_0': np.random.random(1),
    }

    key_df = get_encryption(
        audio.shape[0],
        **encryption_key
    )

