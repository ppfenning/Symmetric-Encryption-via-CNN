import numpy as np
import pandas as pd
from conversion import dec_to_bin
from chaos import (
    sim_chaotic_attractor,
    henon,
    ikeda,
    lorenz,
    logistic
)


def __transform(data):
    return np.mod(np.floor(np.abs(data) * 10 ** 10), 256).astype(np.int16)


def __get_bin(data):
    return pd.DataFrame({
        f"key{n}": dec_to_bin(col)
        for n, col in enumerate(data.T)
    })


def get_public_key(byte_len, *, throw_away, henon_0, ikeda_0, lorenz_0, logistic_0):
    series_len = byte_len + throw_away
    return __get_bin(__transform(np.concatenate((
        sim_chaotic_attractor(henon, series_len, henon_0),
        sim_chaotic_attractor(ikeda, series_len, ikeda_0),
        sim_chaotic_attractor(lorenz, series_len, lorenz_0),
        sim_chaotic_attractor(logistic, series_len, logistic_0)
    ), axis=1))).loc[throw_away:].reset_index(drop=True)
