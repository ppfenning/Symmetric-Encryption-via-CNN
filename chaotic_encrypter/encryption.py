import numpy as np
import re
from numba import njit
from .keygen import ChaosKey


def chaotic_cipher(cipher_len, chaos_maps, str_type, byte_len):

    # get functions and dimensionality
    dims = 0

    for cmap in chaos_maps.values():
        dims += cmap["dim"]

    # set memory for attractor
    attractors = np.zeros((dims, cipher_len), dtype=np.float64)
    i = 0
    for cmap in chaos_maps.values():
        dim = cmap["dim"]
        primer = cmap["primer"]
        steps = cipher_len + primer
        attractors[i:i + dim, :] = __transform(cmap["func"](steps), byte_len)[:, primer:]
        i += dim
    return xor(attractors, str_type)





@njit
def __transform(data, byte_len):
    """
    The __transform function takes in a numpy array of data and the dtype of the data.
    It then returns an array with values that are within the range of 0 to 2^n-2, where n is
    the number of bits in each value. This is accomplished by taking absolute values, multiplying
    by 10^10 (to ensure all numbers have at least 10 decimal places), rounding down to nearest integer,
    and then modding by 2^n-2.

    :param data: Store the data that is to be transformed
    :param dtype: Specify the data type of the output array
    :return: A numpy array of the input data in a specified bit format
    :doc-author: Trelent
    """
    return np.mod(np.floor(data * 10 ** (byte_len/2)), 2**byte_len)


def xor(columns, str_type):
    return np.bitwise_xor.reduce(columns.astype(f"u{str_type}")).astype(str_type)


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
    call_chaos_key = ChaosKey()
    chaos_key = call_chaos_key(chaos_key_path)
    cipher = chaotic_cipher(audio.shape[0], chaos_key, str_type, byte_len)
    return __get_new_audio(audio, cipher, str_type)
