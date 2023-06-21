from pathlib import Path
import pandas as pd
import numpy as np

datadir = Path('../data')
wavedir = datadir.joinpath('wav48')
id_map = pd.read_csv(datadir.joinpath('speaker-info.txt')).set_index('ID', drop=True).to_dict(orient='index')


def get_fpath(speaker_id, section_no):
    return wavedir.joinpath(f"p{speaker_id}/p{speaker_id}_{section_no:03}.wav")


def dec_to_bin(data):
    return pd.Series(data).apply(bin)


def bin_to_dec(data):
    return data.apply(lambda x: int(x, 2)).to_numpy().astype(np.int16)
