from pathlib import Path
import numpy as np
from os import getenv
from reader import read_wav
from chaos import (
    sim_chaotic_attractor,
    henon,
    lorenz,
    ikeda
)
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
    sol = sim_chaotic_attractor(ikeda, [0, 0], np.linspace(0, 4, data.shape[0]))

