from pathlib import Path

import seaborn as sns
from matplotlib import pyplot as plt

from plotters.helpers.coincidence import get_mean_accs, gaussian_fit


sns.set()
sns.set_context(rc={'patch.linewidth': 0.0})


DATA_DIR = Path("../data/swabian/coincidences")
FILE = [
       "ring-12 binwidth_100ps trigger_0.07V power_7dBm 2023-12-13 "
       "10-49-54.csv",
       "ring-24 binwidth_100ps trigger_0.09V power_8dBm 2023-12-12 "
       "10-01-30.csv",
]

plt.figure()

file_path = DATA_DIR / FILE[0]
delay, coins, binwidth, popt, fit_data = gaussian_fit(file_path)

plt.bar(
       delay,
       coins,
       # color='g',
       alpha=0.8,
       width=binwidth,
       label="ring 12",
)

file_path = DATA_DIR / FILE[1]
delay, coins, binwidth, popt, fit_data = gaussian_fit(file_path)

plt.bar(
       delay,
       coins,
       # color='b',
       alpha=0.8,
       width=binwidth,
       label="ring 24",
)

plt.locator_params(axis='x', nbins=10)  # Limit x-axis ticks
plt.xlabel("delay / ps")
plt.ylabel("coincidences / bin")
plt.legend()
plt.title("Ring 12 vs 24 coincidences over 60 s")
plt.savefig(r"figures/ring_12_vs_24_coins.png")
plt.show()