from pathlib import Path

from matplotlib import pyplot as plt

from plotters.helpers.coincidence import plot_coincidences


DATA_DIR = Path("../data/swabian/coincidences")
FILE = "ring-12 binwidth_10ps trigger_0.07V power_7dBm integration_180s " \
       "2023-12-13 10-57-31.csv"

plot_coincidences(DATA_DIR / FILE)
plt.title("Ring 12 at 7 dBm for 180 s")
plt.savefig(r"figures/ring_12_7dBm_coins.png")
plt.show()
