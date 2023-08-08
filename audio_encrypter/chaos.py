from scipy.integrate import odeint
from numba import njit, cfunc
import numpy as np


def __ode_runner(func, v0, t, args):
    return odeint(func, v0, t, args)


def ode_wrapper(func, byte_len, v0, primer, params):
    t = np.linspace(0, 1, byte_len + primer)
    args = tuple(params.values())
    return __ode_runner(func, v0, t, args)[primer:]


def chaotic_functions(chaos_key):
    chaos_key["henon"]["func"] = henon
    chaos_key["ikeda"]["func"] = ikeda
    chaos_key["lorenz"]["func"] = lorenz
    chaos_key["logistic"]["func"] = logistic
    return chaos_key


def chaotic_cipher(audio_len, chaos_key):
    if byte_len := audio_len - chaos_key["bytes_cached"] > 0:
        chaos_key = chaotic_functions(chaos_key)
        for vals in chaos_key.values():
            print(vals)
    return chaos_key



@njit
def henon(v0, t, *params):
    """
    The henon function is a simple function that takes in three parameters:
        v0, t, and a=1.4, b=0.3. The first parameter is the initial value of x and y
        (v0), the second parameter is time (t), and the third parameter are two
        constants that can be changed to alter how quickly or slowly the henon
        attractor converges to its final state.

    :param v0: Set the initial values of x and y
    :param t: Determine the number of steps to take in the
    :param a: Control the strength of the nonlinearity
    :param b: Control the x-axis scaling
    :return: A tuple of values
    :doc-author: Trelent
    """

    a = params[0]
    b = params[1]

    x = v0[0]
    y = v0[1]

    return 1 - a * x ** 2 + y, b * x


@njit
def lorenz(v0, t, *params):
    """
    The lorenz function is a function that takes in three parameters: v0, t, and sigma.
    The first parameter is the initial conditions of the system (x0, y0, z0). The second parameter
    is time. The third parameter is sigma which represents how much energy it takes to move from one state to another.

    :param v0: Set the initial conditions for the system
    :param t: Define the time interval
    :param sigma: Control the strength of the coupling between x and y
    :param beta: Control the rate of divergence of nearby trajectories
    :param rho: Control the strength of the nonlinearity in
    :return: The derivatives of the variables x, y and z
    :doc-author: Trelent
    """
    sigma = params[0]
    beta = params[1]
    rho = params[2]
    
    x = v0[0]
    y = v0[1]
    z = v0[2]
    
    return sigma * (y - x), x * (rho - z) - y, x * y - beta * z


@njit
def ikeda(v0, t, *params):
    """
    The ikeda function is a nonlinear dynamical system that produces
    a chaotic attractor.  The function takes three parameters: mu, beta, and gamma.
    The default values for these parameters are 0.7, 0.4 and 6 respectively.

    :param v0: Set the initial conditions for the system
    :param t: Calculate the time
    :param mu: Control the size of the spiral
    :param beta: Control the number of lobes in the attractor
    :param gamma: Control the size of the spiral
    :return: A tuple of x and y coordinates
    :doc-author: Trelent
    """
    mu = params[0]
    beta = params[1]
    gamma = params[2]

    x = v0[0]
    y = v0[1]

    t_n = beta - gamma/(1 + x**2 + y**2)

    return 1 + mu * (x * np.cos(t_n)) - y * np.sin(t_n), mu * (x * np.sin(t_n) + y * np.cos(t_n))


@njit
def logistic(v0, t, *params):
    """
    The logistic function is a sigmoid function that takes in an input value and returns a value between 0 and 1.
    It is used to model the growth of populations, where the population size can never exceed some maximum.
    The logistic function has two parameters: r, which controls how fast the population grows, and k, which represents
    the carrying capacity of the environment.

    :param v0: Set the initial value of the function
    :param t: Specify the time interval for which we want to calculate the logistic function
    :param r: Control the growth rate of the population
    :return: A value between 0 and 1
    :doc-author: Trelent
    """
    r = params[0]

    x = v0[0]

    return r * x * (1 - x)
