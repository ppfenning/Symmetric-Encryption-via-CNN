from pathlib import Path
import numpy as np
import pandas as pd
from os import getenv
from reader import read_wav
from chaos import get_key
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
    rate, data = read_wav(get_speaker_file(340, 340))
    bin_df = pd.DataFrame(dec_to_bin(data), columns=['audio'])
    soln = get_key(data.shape[0], np.random.random(2), np.random.random(2), np.random.random(3), np.random.random(1))
    for n, col in enumerate(soln.T):
        bin_df[f"key{n}"] = dec_to_bin(col)

