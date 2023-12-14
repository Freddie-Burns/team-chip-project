import numpy as np
import pandas as pd
from scipy.optimize import curve_fit


def gaussian(x, a, mu, sig):
    """Function for scipy.curve_fit to fit data to."""
    return a * np.exp(-np.power((x - mu) / sig, 2) / 2)


def calculate_car(filepath):
    datum = pd.read_csv(
        filepath,
        header=None,
        names=["delay", "coincidences"],
    )

    delay = np.array(datum["delay"])
    coins = np.array(datum["coincidences"])
    binwidth = delay[1] - delay[0]

    # Fit Gaussian to data
    guess = (max(coins), 0, 100)
    popt, pcov = curve_fit(gaussian, delay, coins, guess)
    a, mu, sig = popt

    # True for points over 3 std away from centre of gaussian
    mask = abs(delay - mu) > 4 * sig
    all_accs = coins[mask]
    mean_accs = np.mean(all_accs)

    # Count coincidences within widening windows up to 3 std
    windows = np.arange(binwidth, int(3 * sig), binwidth)
    cars = []
    for width in windows:
        mask = abs(delay - mu) < width
        counts = np.sum(coins[mask])
        accs = mean_accs * len(coins[mask])
        car = counts / accs
        cars.append(car)
    return max(cars)
