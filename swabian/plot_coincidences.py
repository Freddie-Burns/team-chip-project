from pathlib import Path

import pandas as pd
from matplotlib import pyplot as plt


COLORS = ['b', 'g', 'r', 'c', 'm', 'y']

DATA_DIR = Path("../data/swabian/coincidences")
FILES = ["ring-12 binwidth_10ps trigger_0.07V power_7dBm integration_180s 2023-12-13 10-57-31.csv"]

ax = plt.subplot()

for i, file in enumerate(FILES):
    color = COLORS[i % len(COLORS)]
    datum = pd.read_csv(
        DATA_DIR / file,
        header=None,
        names=["delay / ps", "coincidences"],
    )

    datum.plot.bar(
        x="delay / ps",
        y="coincidences",
        ax=ax,
        color=color,
        alpha=0.5,
        width=1,
        label=file[:-4],  # Remove .csv from label
    )

plt.locator_params(axis='x', nbins=10)  # Limit x-axis ticks
plt.show()
