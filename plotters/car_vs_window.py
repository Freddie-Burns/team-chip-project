from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.optimize import curve_fit

from helpers.utils import gaussian


sns.set()


DATA_DIR = Path("../data/swabian/coincidences")
FILE = "ring-12 binwidth_10ps trigger_0.07V power_7dBm integration_180s " \
       "2023-12-13 10-57-31.csv"


filepath = DATA_DIR / FILE
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

# Count coincidences within widening windows up to 3 std
half_widths = np.arange(binwidth, int(2 * sig), binwidth)
cars = []
for widths in half_widths:
    mask = abs(delay - mu) < widths
    counts = np.sum(coins[mask])
    accs = mean_accs * len(coins[mask])
    car = counts / accs
    cars.append(car)

ax = plt.subplot()
fwhm = 2.355 * sig
plt.vlines(fwhm, 0, max(cars), 'k', ':')
ax.text(fwhm + 8, 1, f"FWHM", rotation=90)

plt.scatter(half_widths * 2, cars, marker='x')
plt.xlabel("window / pm")
plt.ylabel("CAR")
plt.title("Ring 12 CAR vs window")
plt.savefig(r"figures/car_vs_window.png")
plt.show()
