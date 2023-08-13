from scipy.integrate import solve_ivp, odeint
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
    xored = np.zeros((cipher_len, 8), dtype=np.float64)
    i = 0
    for maps in ["henon", "ikeda", "lorenz", "logistic"]:
        chaos_map = chaos_inputs[maps]
        func = chaos_map["func"]
        v0 = np.array(chaos_map["v0"])
        params = tuple(chaos_map["params"].values())
        columns = func(v0, cipher_len, params)
        dim = len(v0)
        xored[:, i:i+dim] = columns
        i += dim
    return xor(__transform(xored, byte_len), str_type, 1)


@njit
def __henon(v0, *params):

    a = params[0]
    b = params[1]

    x = v0[0]
    y = v0[1]

    return 1 - a * x * x + y, b * x


def henon(v0, steps, params):
    out_val = np.zeros((steps, 2))
    for i in range(steps):
        out_val[i] = v0
        v0 = __henon(v0, *params)
    return out_val

@njit
def __lorenz(t, state, sigma, rho, beta):
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]


def lorenz(v0, steps, params):
    t_span = (0, 40)
    t_eval = np.linspace(*t_span, steps)
    sol = solve_ivp(
        fun=__lorenz,
        t_span=t_span,
        y0=v0,
        args=params,
        t_eval=t_eval,
        method='RK45'
    )
    return sol.y.T


@njit
def __ikeda(v0, *params):

    mu = params[0]
    beta = params[1]
    gamma = params[2]

    x = v0[0]
    y = v0[1]

    t_n = beta - (gamma / (1 + x * x + y * y))

    return 1 - 1 + mu * (x * np.cos(t_n)) - y * np.sin(t_n), mu * (x * np.sin(t_n) + y * np.cos(t_n))


def ikeda(v0, steps, params):
    out_val = np.zeros((steps, 2))
    for i in range(steps):
        out_val[i] = v0
        v0 = __ikeda(v0, *params)
    return out_val


@njit
def __logistic(v0, steps, *params):

    r = params[0]
    x = v0[0]
    out_val = np.zeros((steps, 1))

    for i in range(steps):
        out_val[i] = x
        x = r * x * (1 - x)

    return out_val


def logistic(v0, steps, params):
    return __logistic(v0, steps, *params)
