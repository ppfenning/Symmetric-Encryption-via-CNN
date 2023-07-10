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


def __get_chaos_key(keypath: Path):
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


def __chaotic_cipher(audio_len, str_type, *, throw_away, henon_0, ikeda_0, lorenz_0, logistic_0, ):
    file_len = audio_len + throw_away
    return __transform(
        np.concatenate((
            sim_chaotic_attractor(henon, file_len, henon_0),
            sim_chaotic_attractor(ikeda, file_len, ikeda_0),
            sim_chaotic_attractor(lorenz, file_len, lorenz_0),
            sim_chaotic_attractor(logistic, file_len, logistic_0)
        ), axis=1)
        , str_type
    )[throw_away:]


def __chaotic_ciphertext(audio, chaos_key):
    str_type = audio.dtype.name
    cipher = __chaotic_cipher(audio.size, str_type, **chaos_key)
    combo = np.append(audio[:, np.newaxis], cipher, axis=1)
    return np.bitwise_xor.reduce(combo.astype(f'u{str_type}'), axis=1).astype(str_type)


def chaotic_ciphertext(audio, keypath):
    return __chaotic_ciphertext(audio, __get_chaos_key(keypath))
