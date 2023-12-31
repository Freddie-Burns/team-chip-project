import os
from pathlib import Path

import pandas as pd
from matplotlib import pyplot as plt


CHANNELS = range(30, 41)
DWDM_DIR = Path("../data/dwdm")
XLIM = (1544.5, 1554)
YLIM = (-30, -5)


channel_number = None
dwdm_filenames = []
channels = []
ax = plt.subplot()


# Plot DWDM channel transmissions *********************************************


for dwdm_filename in os.listdir(DWDM_DIR):
    try:
        channel_number = int(dwdm_filename[8:10])
        if channel_number in CHANNELS:
            dwdm_filenames.append(dwdm_filename)
            channels.append(channel_number)
    except ValueError:
        pass  # Some files will not have a channel number

for i, filename in enumerate(dwdm_filenames):
    file_path = DWDM_DIR / filename
    datum = pd.read_csv(
        file_path,
        header=None,
        names=["wavelength", "transmission"],
    )
    datum.plot(
        kind='line',
        x="wavelength",
        y="transmission",
        ax=ax,
    )


# Plot all DWDM channel central wavelengths as dotted lines *******************


channels = pd.read_csv(DWDM_DIR / "channel_wavelength_table.csv")
for i in channels.index:
    channel = channels.iloc[i]["channel"]
    if channel not in CHANNELS: continue  # Don't include this channel
    wavelength = channels.iloc[i]["wavelength"]
    ax.vlines(wavelength, *YLIM, 'k', ':')
    ax.text(wavelength-0.1, YLIM[1]+0.6, f"{int(channel)}", rotation=90)


# Format plot *****************************************************************


plt.ylim(YLIM)
plt.xlim(XLIM)
plt.xlabel("wavelength / nm")
plt.ylabel("transmission / dB")
ax.get_legend().remove()
plt.savefig(r"figures/dwdm_transmission.png")
plt.show()
