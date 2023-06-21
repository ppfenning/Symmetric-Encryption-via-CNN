import pandas as pd
import numpy as np


def dec_to_bin(data: np.ndarray) -> pd.Series:
    return pd.Series(data).apply(bin)


def bin_to_dec(data: pd.Series) -> np.ndarray:
    return data.apply(lambda x: int(x, 2)).to_numpy().astype(np.int16)
