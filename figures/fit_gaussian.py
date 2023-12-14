from pathlib import Path

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

from utils import gaussian

DATA_DIR = Path("../data/swabian/coincidences")
FILE = "ring-12 binwidth_10ps trigger_0.07V power_7dBm integration_180s 2023-12-13 10-57-31.csv"


datum = pd.read_csv(
    DATA_DIR / FILE,
    header=None,
    names=["delay", "coincidences"],
)

delay = np.array(datum["delay"])
coins = np.array(datum["coincidences"])
binwidth = delay[1] - delay[0]

# Fit Gaussian to data
popt, pcov = curve_fit(gaussian, delay, coins)
a, mu, sig = popt
fit_data = gaussian(delay, *popt)

plt.figure()

plt.bar(
    delay,
    coins,
    color='g',
    alpha=0.5,
    width=binwidth,
    label=FILE[:7],  # Device name only
)

plt.plot(
    delay,
    fit_data,
    color='b',
    linestyle=':',
    label="Gaussian fit",
)

# Plot standard deviations
# ylim = ax.get_ylim()
# ax.vlines([mu-sig, mu+sig], *ylim)
# ax.vlines([mu-3*sig, mu+3*sig], *ylim)

# True for points over 3 std away from centre of gaussian
mask = abs(delay - mu) > 4 * sig
all_accs = coins[mask]
mean_accs = np.mean(all_accs)

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

# Count coincidences within widening windows up to 3 std
windows = np.arange(binwidth, int(3 * sig), binwidth)
cars = []
for width in windows:
    mask = abs(delay - mu) < width
    counts = np.sum(coins[mask])
    accs = mean_accs * len(coins[mask])
    car = counts / accs
    cars.append(car)

plt.figure()
plt.scatter(windows * 2, cars)
plt.xlabel("coincidence window / ps")
plt.ylabel("CAR")

plt.show()
