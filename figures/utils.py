import numpy as np


def gaussian(x, a, mu, sig):
    """Function for scipy.curve_fit to fit data to."""
    return a * np.exp(-np.power((x - mu) / sig, 2) / 2)
