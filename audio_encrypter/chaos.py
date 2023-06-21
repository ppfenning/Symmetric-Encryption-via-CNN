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
