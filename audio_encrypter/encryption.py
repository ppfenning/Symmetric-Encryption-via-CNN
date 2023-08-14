import yaml
from pathlib import Path
import numpy as np
from audio_encrypter.chaos import chaotic_cipher, xor
import re


def __init_key(keypath: Path):
    keypath.parent.mkdir(parents=True, exist_ok=True)
    chaos_key = {
        'primer': int(np.random.randint(1, 1000, 1)),
        'henon_1': {
            "map": "henon",
            "params": dict(zip(["a", "b"], [1.4, 0.3])),
            "v0": np.random.uniform(-0.1, 0.1, 2).tolist()
        },
        'ikeda_1': {
            "map": "ikeda",
            "params": dict(zip(["mu", "beta", "gamma"], [0.7, 0.4, 6])),
            "v0": np.random.uniform(-10, 10, 2).tolist()
        },
        'lorenz_1': {
            "map": "lorenz",
            "params": dict(zip(["sigma", "beta", "rho"], [10, 8 / 3, 28])),
            "v0": np.random.uniform(-10, 10, 3).tolist()
        },
        'logistic_1': {
            "map": "logistic",
            "params": dict(zip(["r"], [4])),
            "v0": np.random.random(1).tolist()
        },
    }
    with keypath.open('w') as writer:
        yaml.dump(chaos_key, writer)
    return chaos_key


def __get_chaos_key(keypath: Path):
    """
    The __get_chaos_key function is used to generate a random seed for the chaos functions.
    The keypath argument is a pathlib Path object that points to where the file should be saved.
    If it does not exist, then it will create one with random values and save it there. If it does exist, then
    it will load those values from that file and return them as a dictionary.

    :param keypath: Path: Specify the path to the key file
    :return: A dictionary of the form:
    :doc-author: Trelent
    """
    if not keypath.exists():
        return __init_key(keypath)
    with keypath.open('r') as reader:
        return yaml.safe_load(reader.read())


def __get_new_audio(audio, cipher, str_type):
    if audio.ndim == 1:
        return xor(np.array([audio, cipher]), str_type)
    else:
        new_audio = np.zeros(audio.shape, dtype=str_type)
        for i, channel in enumerate(audio.T):
            new_audio[:, i] = xor(np.array([channel, cipher]), str_type)
        return new_audio


def chaotic_ciphertext(audio, chaos_key_path):
    str_type = audio.dtype.name
    byte_len = int(re.findall(r'\d+', str_type)[0])
    chaos_key = __get_chaos_key(chaos_key_path.joinpath("key.yaml"))
    primer = chaos_key["primer"]
    cipher_len = primer + audio.shape[0]
    return __get_new_audio(
        audio,
        chaotic_cipher(cipher_len, chaos_key, str_type, byte_len)[primer:],
        str_type
    )
