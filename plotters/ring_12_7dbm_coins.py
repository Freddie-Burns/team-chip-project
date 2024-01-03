from pathlib import Path

import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

from helpers.coincidence import gaussian_fit, get_mean_accs


sns.set()
sns.set_context(rc={'patch.linewidth': 0.0})


DATA_DIR = Path("../data/swabian/coincidences")
FILE = "ring-12 binwidth_10ps trigger_0.07V power_7dBm integration_180s " \
       "2023-12-13 10-57-31.csv"

file_path = DATA_DIR / FILE

delay, coins, binwidth, popt, fit_data = gaussian_fit(file_path)
a, mu, sig = popt

plt.figure()

plt.bar(
       delay,
       coins,
       # color='g',
       alpha=0.8,
       width=binwidth,
       label="coincidences",
)

plt.plot(
       delay,
       fit_data,
       color='k',
       linestyle='--',
       label="Gaussian fit",
)

mean_accs = get_mean_accs(delay, coins, mu, sig)
plt.plot(
       delay,
       mean_accs * np.ones(delay.shape),
       color='r',
       linestyle='--',
       label="mean accidentals",
)

plt.locator_params(axis='x', nbins=10)  # Limit x-axis ticks
plt.xlabel("delay / ps")
plt.ylabel("coincidences / bin")
plt.legend()


plt.title("Ring 12 at 7 dBm for 180 s")
plt.savefig(r"figures/ring_12_7dBm_coins.png")
plt.show()
