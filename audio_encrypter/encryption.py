import pickle
from pathlib import Path
import numpy as np
from chaos import (
    sim_chaotic_attractor,
    henon,
    ikeda,
    lorenz,
    logistic
)


def __transform(data):
    return np.mod(np.floor(np.abs(data) * 10 ** 10), 2**16).astype(np.uint16)


def get_key(keypath: Path, throw_away):
    if not keypath.exists():
        keypath.parent.mkdir(parents=True, exist_ok=True)
        with keypath.open('wb') as writer:
            pickle.dump(
                {
                    'throw_away': throw_away,
                    'henon_0': np.random.random(2),
                    'ikeda_0': np.random.random(2),
                    'lorenz_0': np.random.random(3),
                    'logistic_0': np.random.random(1),
                }
                , writer
            )
    with keypath.open('rb') as reader:
        return pickle.loads(reader.read())


def get_encryption(audio, *, throw_away, henon_0, ikeda_0, lorenz_0, logistic_0):
    file_len = audio.size + throw_away
    encryption = __transform(np.concatenate((
        sim_chaotic_attractor(henon, file_len, henon_0),
        sim_chaotic_attractor(ikeda, file_len, ikeda_0),
        sim_chaotic_attractor(lorenz, file_len, lorenz_0),
        sim_chaotic_attractor(logistic, file_len, logistic_0)
    ), axis=1))[throw_away:]
    combo = np.append(audio[:, np.newaxis], encryption, axis=1).astype(np.uint16)
    return np.bitwise_xor.reduce(combo, axis=1).astype(np.int16)



