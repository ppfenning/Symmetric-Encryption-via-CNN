import pickle
import re
from pathlib import Path
import numpy as np
from .chaos import (
    sim_chaotic_attractor,
    henon,
    ikeda,
    lorenz,
    logistic
)


def __transform(data, dtype):
    return np.mod(np.floor(np.abs(data) * 10 ** 10), 2**int(re.findall(r'\d+', dtype)[0]))


def get_key(keypath: Path):
    if not keypath.exists():
        keypath.parent.mkdir(parents=True, exist_ok=True)
        with keypath.open('wb') as writer:
            pickle.dump(
                {
                    'throw_away': int(np.random.randint(1000, 10000, 1)),
                    'henon_0': np.random.random(2),
                    'ikeda_0': np.random.random(2),
                    'lorenz_0': np.random.random(3),
                    'logistic_0': np.random.random(1),
                }
                , writer
            )
    with keypath.open('rb') as reader:
        return pickle.loads(reader.read())


def __get_encryption(audio, *, throw_away, henon_0, ikeda_0, lorenz_0, logistic_0):
    file_len = audio.size + throw_away
    str_type = audio.dtype.name
    encryption = __transform(
        np.concatenate((
            sim_chaotic_attractor(henon, file_len, henon_0),
            sim_chaotic_attractor(ikeda, file_len, ikeda_0),
            sim_chaotic_attractor(lorenz, file_len, lorenz_0),
            sim_chaotic_attractor(logistic, file_len, logistic_0)
        ), axis=1)
        , str_type
    )[throw_away:]
    combo = np.append(audio[:, np.newaxis], encryption, axis=1)
    return np.bitwise_xor.reduce(combo.astype(f'u{str_type}'), axis=1).astype(str_type)


def get_encryption(audio, keypath):
    return __get_encryption(audio, **get_key(keypath))
