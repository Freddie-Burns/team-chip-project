"""
Plot of main central peak and side peaks of unknown origin.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


sns.set()
sns.set_context(rc={'patch.linewidth': 0.0})


DATA_DIR = Path("../data/swabian/coincidences")
FILE = "ring-12 binwidth_1000ps trigger_0.07V power_7dBm 2023-12-13 " \
       "10-47-40.csv"
SAVE_PATH = Path("figures") / "side_peaks.png"

file_path = DATA_DIR / FILE
datum = pd.read_csv(
       file_path,
       header=None,
       names=["delay", "coincidences"],
)

delay = np.array(datum["delay"]) / 1000
coins = np.array(datum["coincidences"])
binwidth = delay[1] - delay[0]

plt.figure()
plt.bar(
       delay,
       coins,
       # color='g',
       # alpha=0.5,
       width=binwidth,
       label="coincidences",
)
plt.title("Ring 12 coincidence side peaks")
plt.xlabel("delay / ns")
plt.ylabel("coincidences / bin")
plt.savefig(SAVE_PATH)
plt.show()
