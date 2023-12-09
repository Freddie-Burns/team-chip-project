import os
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


DWDM_CHANNELS = range(30, 40)
DWDM_DIR = Path("../data/dwdm")
Y_LIM = (-20, 0)

ax = plt.subplot()
plt.ylim(Y_LIM)

dwdm_filenames = []
channel_number = None

channels = pd.read_csv(DWDM_DIR / "channel wavelength table.csv")
plt.vlines(channels["Wavelength"], *Y_LIM, 'k', ':')

for dwdm_filename in os.listdir(DWDM_DIR):
    try: channel_number = int(dwdm_filename[8:10])
    except ValueError: pass

    if channel_number in DWDM_CHANNELS:
        dwdm_filenames.append(dwdm_filename)

dwdm_data = []
for filename in dwdm_filenames:
    file_path = DWDM_DIR / filename
    datum = pd.read_csv(
        file_path, header=None, names=["wavelength", "transmission"])
    datum.plot(kind='line', x="wavelength", y="transmission", ax=ax)

plt.show()
