from scipy.integrate import solve_ivp
from numba import njit
import numpy as np


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


def henon(v0, params, steps):
    return __henon(v0, steps, *params)


@njit
def __lorenz(t, state, sigma, rho, beta):
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]


def lorenz(v0, params, steps):
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
    return sol.y


@njit
def __ikeda(v0, steps, *params):

    mu = params[0]

    x = v0[0]
    y = v0[1]

    out_val = np.zeros((2, steps))

    for i in np.arange(0, steps):
        out_val[0, i] = x
        out_val[1, i] = y
        t_n = 0.4 - (6 / (1 + x*x + y*y))
        x, y = 1 + mu*(x*np.cos(t_n) - y*np.sin(t_n)), mu*(x*np.sin(t_n) + y*np.cos(t_n))

    return out_val


def ikeda(v0, params, steps):
    return __ikeda(tuple(v0), steps, *params)


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


def tinkerbell(v0, params, steps):
    return __tinkerbell(v0, steps, *params)


@njit
def __logistic(v0, steps, *params):

    r = params[0]
    x = v0[0]

    out_val = np.zeros((1, steps))

    for i in np.arange(0, steps):
        out_val[0, i] = x
        x = r*x*(1 - x)

    return out_val


def logistic(v0, params, steps):
    return __logistic(v0, steps, *params)
