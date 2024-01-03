from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit


RING_12_FILES = [
    "ring-12 binwidth_10ps trigger_0.07V power_1dBm integration_120s "
    "2023-12-13 11-22-28.csv",
    "ring-12 binwidth_10ps trigger_0.07V power_2dBm integration_120s "
    "2023-12-13 11-15-32.csv",
    "ring-12 binwidth_10ps trigger_0.07V power_3dBm integration_120s "
    "2023-12-13 11-12-05.csv",
    "ring-12 binwidth_10ps trigger_0.07V power_4dBm integration_120s "
    "2023-12-13 11-09-40.csv",
    "ring-12 binwidth_10ps trigger_0.07V power_5dBm integration_120s "
    "2023-12-13 11-07-15.csv",
    "ring-12 binwidth_10ps trigger_0.07V power_6dBm integration_120s "
    "2023-12-13 11-04-50.csv",
    "ring-12 binwidth_10ps trigger_0.07V power_7dBm integration_180s "
    "2023-12-13 10-57-31.csv",
]


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
    mask = abs(delay - mu) > 3 * sig
    all_accs = coins[mask]
    mean_accs = np.mean(all_accs)

    # Count coincidences within FWHM of fitted Gaussian
    mask = abs(delay - mu) < 1.78 * sig
    counts = np.sum(coins[mask])
    accs = mean_accs * len(coins[mask])
    return counts / accs


def calculate_brightness(filepath, time, power):
    """
    Args: time in seconds, power in dBm, wavelength in nm.
    Returns: brightness in pairs/s/mW^2
    """
    # Convert dBm to mW
    power = 10 ** (power / 10)

    datum = pd.read_csv(
        filepath,
        header=None,
        names=["delay", "coincidences"],
    )

    delay = np.array(datum["delay"])
    coins = np.array(datum["coincidences"])

    # Fit Gaussian to data
    guess = (max(coins), 0, 100)
    popt, pcov = curve_fit(gaussian, delay, coins, guess)
    a, mu, sig = popt

    # Calculate number of
    mask = abs(delay - mu) > 3 * sig
    mean_accs = np.mean(coins[mask])
    all_coins = np.sum(coins) - mean_accs * len(delay)

    return all_coins / (time * power**2)



