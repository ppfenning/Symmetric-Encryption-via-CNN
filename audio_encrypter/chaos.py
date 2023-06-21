from scipy.integrate import odeint


def sim_chaotic_array(func, v0, t, **kwargs):
    return odeint(func, v0, t, tuple(kwargs))


def henon(v0, t, a=1.4, b=0.3):
    """Henon attractor"""
    x, y = v0
    return 1 - a * x ** 2 + y, b * x


def lorenz(v0, t, sigma=10, beta=8/3, rho=28):
    """The Lorenz equations."""
    x, y, z = v0
    return sigma * (y - x), x * (rho - z) - y, x * y - beta * z


def ikeda(): pass


def logistic(): pass