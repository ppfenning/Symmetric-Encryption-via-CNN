from pathlib import Path
import numpy as np
import pandas as pd
from os import getenv
from reader import read_wav
from chaos import get_public_key
from conversion import dec_to_bin
from dotenv import load_dotenv

env_file = Path("../config/.env")

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
    k, n = 1000, audio.shape[0]
    key_df = get_public_key(k, n, np.random.random(2), np.random.random(2), np.random.random(3), np.random.random(1))

