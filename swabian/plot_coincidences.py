from pathlib import Path
import os

import pandas as pd
from matplotlib import pyplot as plt


COLOURS = ['b', 'g', 'r', 'c', 'm', 'y']

DATA_DIR = Path("../data/swabian")
FILES = os.listdir(DATA_DIR)

ax = plt.subplot()

for i, file in enumerate(FILES):
    datum = pd.read_csv(
        DATA_DIR / file,
        header=None,
        names=["delay / ps", "coincidences"],
    )

    datum.plot.bar(
        x="delay / ps",
        y="coincidences",
        ax=ax,
        color=COLOURS[i],
        width=1,
        label=file[:-4],  # Remove .csv from label
    )

plt.show()
