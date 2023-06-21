from scipy.integrate import odeint
from conversion import dec_to_bin
import numpy as np
import pandas as pd


def sim_chaotic_attractor(func, n, v0, **kwargs):
    t = np.linspace(0, 1, n)
    return odeint(func, v0, t, tuple(kwargs))


def henon(v0, t, a=1.4, b=0.3):
    """Henon attractor"""
    x, y = v0
    return 1 - a * x ** 2 + y, b * x


def lorenz(v0, t, sigma=10, beta=8/3, rho=28):
    """The Lorenz equations."""
    x, y, z = v0
    return sigma * (y - x), x * (rho - z) - y, x * y - beta * z


def ikeda(v0, t, mu=0.7, beta=0.4, gamma=6):
    x, y = v0
    t_n = beta - gamma/(1 + x**2 + y**2)
    return 1 + mu * (x * np.cos(t_n)) - y * np.sin(t_n), mu * (x * np.sin(t_n) + y * np.cos(t_n))


def logistic(v0, t, r=4):
    return r * v0[0] * (1 - v0[0])


def __transform(data):
    return np.mod(np.floor(np.abs(data) * 10 ** 10), 256).astype(np.int16)


def __get_bin(data):
    return pd.DataFrame({
        f"key{n}": dec_to_bin(col)
        for n, col in enumerate(data.T)
    })


def get_key(n, henon_0, ikeda_0, lorenz_0, logistic_0):
    sol_henon = sim_chaotic_attractor(henon, n, henon_0)
    sol_ikeda = sim_chaotic_attractor(ikeda, n, ikeda_0)
    sol_lorenz = sim_chaotic_attractor(lorenz, n, lorenz_0)
    sol_logistic = sim_chaotic_attractor(logistic, n, logistic_0)
    return __get_bin(__transform(np.concatenate((sol_henon, sol_ikeda, sol_lorenz, sol_logistic), axis=1)))
