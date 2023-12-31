"""
Plot many coincidence files to view at once, not saving any.
"""

from pathlib import Path
from matplotlib import pyplot as plt
from plotters.helpers.coincidence import plot_coincidences


DATA_DIR = Path("../data/swabian/coincidences")
FILES = [
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


for file in FILES:
    plot_coincidences(DATA_DIR / file)
    plt.title(file)

plt.show()
