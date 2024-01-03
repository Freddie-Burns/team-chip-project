import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

from plotters.helpers.utils import gaussian


COLORS = ['b', 'g', 'r', 'c', 'm', 'y']


def gaussian_fit(file_path):
    """
    Plot coincidences against delay as bar chart with Gaussian fit.
    """
    datum = pd.read_csv(
        file_path,
        header=None,
        names=["delay", "coincidences"],
    )

    delay = np.array(datum["delay"])
    coins = np.array(datum["coincidences"])
    binwidth = delay[1] - delay[0]

    # Fit Gaussian to data
    guess = (max(coins), 0, 100)
    popt, pcov = curve_fit(gaussian, delay, coins, guess)  # a, mu, sig = popt
    fit_data = gaussian(delay, *popt)

    return delay, coins, binwidth, popt, fit_data


def get_mean_accs(delay, coins, mu, sig):
    """Return mean accidental count per bin"""
    # True for points over 3 std away from centre of gaussian
    mask = abs(delay - mu) > 4 * sig
    all_accs = coins[mask]
    return np.mean(all_accs)


def plot_coincidences(file_path, ax=None):
    delay, coins, binwidth, popt, fit_data = gaussian_fit(file_path)
    a, mu, sig = popt

    if ax is None: plt.figure()

    plt.bar(
        delay,
        coins,
        color='g',
        alpha=0.5,
        width=binwidth,
        label="coincidences",
    )

    plt.plot(
        delay,
        fit_data,
        color='b',
        linestyle=':',
        label="Gaussian fit",
    )

    mean_accs = get_mean_accs(delay, coins, mu, sig)
    plt.plot(
        delay,
        mean_accs * np.ones(delay.shape),
        color='r',
        label="mean accidentals",
    )

    plt.locator_params(axis='x', nbins=10)  # Limit x-axis ticks
    plt.xlabel("delay / ps")
    plt.ylabel("coincidences / bin")
    plt.legend()


def plot_car_vs_window(file_path):
    """
    Count coincidences within widening windows up to 3 std.
    """
    delay, coins, binwidth, popt, fit_data = gaussian_fit(file_path)
    a, mu, sig = popt

    mean_accs = get_mean_accs(delay, coins, mu, sig)
    windows = np.arange(binwidth, int(3 * sig), binwidth)
    cars = []
    for width in windows:
        mask = abs(delay - mu) < width
        counts = np.sum(coins[mask])
        accs = mean_accs * len(coins[mask])
        car = counts / accs
        cars.append(car)

    plt.figure()
    plt.scatter(windows * 2, cars, marker='x')  # Windows are +- width so 2x
    plt.xlabel("coincidence window / ps")
    plt.ylabel("CAR")
