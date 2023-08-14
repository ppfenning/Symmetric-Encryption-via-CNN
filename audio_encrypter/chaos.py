from scipy.integrate import odeint
from numba import njit
import numpy as np


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


def __get_chaotic_map(map_name):
    if map_name == "henon":
        return henon
    elif map_name == "ikeda":
        return ikeda
    elif map_name == "lorenz":
        return lorenz
    elif map_name == "logistic":
        return logistic
    elif map_name == "tinkerbell":
        return tinkerbell


def chaotic_cipher(cipher_len, chaos_inputs, str_type, byte_len):

    # get functions and dimensionality
    dims = 0

    for key in chaos_inputs.keys():
        if key != "primer":
            dims += len(chaos_inputs[key]["v0"])

    # set memory for attractor
    attractors = np.zeros((dims, cipher_len), dtype=np.float64)
    i = 0
    for key in chaos_inputs.keys():
        if key != "primer":
            chaos_map = chaos_inputs[key]
            v0 = np.array(chaos_map["v0"])
            params = tuple(chaos_map["params"].values())
            dim = len(v0)
            func = __get_chaotic_map(chaos_map["map"])
            attractors[i:i + dim, :] = __transform(func(v0, cipher_len, params), byte_len)
            i += dim
    return xor(attractors, str_type)


@njit
def __henon(v0, steps, *params):

    a = params[0]
    b = params[1]

    x = v0[0]
    y = v0[1]

    out_val = np.zeros((2, steps))

    for i in np.arange(0, steps):
        out_val[0, i] = x
        out_val[1, i] = y
        x, y = 1 - a * x * x + y, b * x

    return out_val


def henon(v0, steps, params):
    return __henon(v0, steps, *params)

@njit
def __lorenz(v0, t, *params):

    sigma = params[0]
    beta = params[1]
    rho = params[2]

    x = v0[0]
    y = v0[1]
    z = v0[2]

    dxdt = sigma*(y - x)
    dydt = x*(rho - z) - y
    dzdt = x*y - beta*z

    return x+dxdt, y+dydt, z+dzdt


def lorenz(v0, steps, params):
    return odeint(__lorenz, v0, np.arange(0, steps), args=params).T


@njit
def __ikeda(v0, steps, *params):

    mu = params[0]
    beta = params[1]
    gamma = params[2]

    x = v0[0]
    y = v0[1]

    out_val = np.zeros((2, steps))

    for i in np.arange(0, steps):
        out_val[0, i] = x
        out_val[1, i] = y
        t_n = beta - (gamma / (1 + x*x + y*y))
        x, y = 1 - 1 + mu * (x * np.cos(t_n)) - y * np.sin(t_n), mu * (x * np.sin(t_n) + y * np.cos(t_n))

    return out_val


def ikeda(v0, steps, params):
    return __ikeda(v0, steps, *params)


@njit
def __tinkerbell(v0, steps, *params):

    a = params[0]
    b = params[1]
    c = params[2]
    d = params[3]

    x = v0[0]
    y = v0[1]

    out_val = np.zeros((2, steps))

    for i in np.arange(0, steps):
        out_val[0, i] = x
        out_val[1, i] = y
        x, y = x*x + y*y + a*x + b*y, 2*x*y + c*x + d*y

    return out_val


def tinkerbell(v0, steps, params):
    return __tinkerbell(v0, steps, *params)


@njit
def __logistic(v0, steps, *params):

    r = params[0]
    x = v0[0]

    out_val = np.zeros(steps)

    for i in np.arange(0, steps):
        out_val[i] = x
        x = r*x*(1 - x)

    return out_val


def logistic(v0, steps, params):
    return __logistic(v0, steps, *params)
