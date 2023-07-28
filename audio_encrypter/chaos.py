from scipy.integrate import odeint
import numpy as np


def sim_chaotic_attractor(func, n, v0, **kwargs):
    """
    The sim_chaotic_attractor function takes in a function, the number of points to be plotted, and an initial value.
    It then returns the values of that function over time using odeint.

    :param func: Specify the function that will be used to calculate the derivative
    :param n: Determine the number of points in the time series
    :param v0: Set the initial conditions for the system
    :param **kwargs: Pass a variable number of keyword arguments to a function
    :return: A numpy array of the values of v
    :doc-author: Trelent
    """
    t = np.linspace(0, 1, n)
    return odeint(func, v0, t, tuple(kwargs))


def henon(v0, t, a=1.4, b=0.3):
    """
    The henon function is a simple function that takes in three parameters:
        v0, t, and a=b=0.3. The first parameter is the initial value of x and y
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
    x, y = v0
    return 1 - a * x ** 2 + y, b * x


def lorenz(v0, t, sigma=10, beta=8/3, rho=28):
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
    x, y, z = v0
    return sigma * (y - x), x * (rho - z) - y, x * y - beta * z


def ikeda(v0, t, mu=0.7, beta=0.4, gamma=6):
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
    x, y = v0
    t_n = beta - gamma/(1 + x**2 + y**2)
    return 1 + mu * (x * np.cos(t_n)) - y * np.sin(t_n), mu * (x * np.sin(t_n) + y * np.cos(t_n))


def logistic(v0, t, r=4):
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
    return r * v0[0] * (1 - v0[0])
