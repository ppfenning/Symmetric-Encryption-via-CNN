from scipy.integrate import odeint
from numba import njit
import numpy as np


def __chaos_runner(func, v0, params):
    return func(v0,  params)


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
    return np.mod(np.floor(np.abs(data) * 10 ** 10), 2**byte_len)


def xor(columns, str_type, axis):
    return np.bitwise_xor.reduce(columns.astype(f"u{str_type}"), axis=axis).astype(str_type)


def chaotic_functions(chaos_inputs):
    chaos_inputs["henon"]["func"] = henon
    chaos_inputs["ikeda"]["func"] = ikeda
    chaos_inputs["lorenz"]["func"] = lorenz
    chaos_inputs["logistic"]["func"] = logistic
    return chaos_inputs


def chaotic_cipher(cipher_len, chaos_inputs, str_type, byte_len):
    chaos_inputs = chaotic_functions(chaos_inputs)
    xored = np.zeros((cipher_len, 9), dtype=str_type)
    t = np.linspace(0, 1, cipher_len)
    i = 0
    for maps in ["henon", "ikeda", "lorenz", "logistic"]:
        chaos_map = chaos_inputs[maps]
        func = chaos_map["func"]
        v0 = np.array(chaos_map["v0"])
        params = tuple(chaos_map["params"].values())
        columns = func(v0, t, params, byte_len)
        dim = len(v0)
        xored[:, i:i+dim] = columns
        i += dim
    return xor(xored, str_type, 1)


@njit
def __henon(v0, t, *params):

    a = params[0]
    b = params[1]

    x = v0[0]
    y = v0[1]

    return 1 - a * x ** 2 + y, b * x


def henon(v0, t, params, byte_len):
    return __transform(odeint(__henon, v0, t, args=params), byte_len)

@njit
def __lorenz(v0, t, *params):
    sigma = params[0]
    beta = params[1]
    rho = params[2]

    x = v0[0]
    y = v0[1]
    z = v0[2]
    
    return sigma * (y - x), x * (rho - z) - y, x * y - beta * z


def lorenz(v0, t, params, byte_len):
    return __transform(odeint(__lorenz, v0, t, args=params), byte_len)


@njit
def __ikeda(v0, t, *params):

    mu = params[0]
    beta = params[1]
    gamma = params[2]

    x = v0[0]
    y = v0[1]

    t_n = beta - gamma/(1 + x**2 + y**2)

    return 1 + mu * (x * np.cos(t_n)) - y * np.sin(t_n), mu * (x * np.sin(t_n) + y * np.cos(t_n))


def ikeda(v0, t, params, byte_len):
    return __transform(odeint(__ikeda, v0, t, args=params), byte_len)


@njit
def __logistic(v0, t, *params):

    r = params[0]
    x = v0[0]

    return np.array([r * x * (1 - x)])


def logistic(v0, t, params, byte_len):
    return __transform(odeint(__logistic, v0, t, args=params), byte_len)
