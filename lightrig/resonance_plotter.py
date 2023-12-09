import os
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


COLOURS = ['b', 'g', 'r', 'c', 'm', 'y']
DWDM_CHANNELS = (24, 31, 37)  # channels to show transmission data
DWDM_DIR = Path("../data/dwdm")
RESONANCE_DIR = Path("../data/resonance")
X_LIM = (1545, 1560)
Y_LIM = (-19, -15)

# Usually only plot one resonance file
# Can plot more than one to compare
# e.g. to see if resonances shift over time
FILES = [
    # "ring-17 2023-12-01 10-49-28.csv",
    "ring-01 2023-12-01 10-40-52.csv",
    "ring-01 2023-12-04 13-50-17.csv",
]


def main():
    # Create matplotlib plot and set y-axis limits
    ax = plt.subplot()
    plt.ylim(Y_LIM)
    plt.xlim(X_LIM)
    plot_channel_centers(ax)
    plot_transmission_data(ax)
    plot_dwdm_transmission(ax)
    plt.show()


def plot_channel_centers(ax):
    """Plot all DWDM channel central wavelengths as dotted lines."""
    channels = pd.read_csv(DWDM_DIR / "channel wavelength table.csv")
    for i in channels.index:
        wavelength = channels.iloc[i]["wavelength"]
        channel = channels.iloc[i]["channel"]
        ax.vlines(wavelength, *Y_LIM, 'k', ':')
        ax.text(wavelength+0.05, Y_LIM[0]+0.05, f"{int(channel)}", rotation=90)


def plot_transmission_data(ax):
    """Plot transmission against frequency for specified csv files."""
    data = []
    for file in FILES:
        datum = pd.read_csv(
            RESONANCE_DIR / file,
            header=None,
            names=["wavelength", "transmission"],
        )
        data.append(datum)

    # Find the highest transmission
    # Adjust all sweeps to this for easier comparison
    maxima = []
    for datum in data:
        maxima.append(datum["transmission"].max())
    max_transmission = max(maxima)
    for datum in data:
        diff = max_transmission - datum["transmission"].max()
        datum["transmission"] += diff

    # Plot adjusted transmission data
    for i, datum in enumerate(data):
        file = FILES[i]
        datum.plot(
            kind='line',
            x="wavelength",
            y="transmission",
            ax=ax,
            label=file[:-3],  # Remove file type from label
        )


def plot_dwdm_transmission(ax):
    """Plot transmission data for specified DWDM channels"""
    channel_number = None
    dwdm_filenames = []
    channels = []

    for dwdm_filename in os.listdir(DWDM_DIR):
        try: channel_number = int(dwdm_filename[8:10])
        except ValueError: pass  # Some files will not have a channel number
        if channel_number in DWDM_CHANNELS:
            dwdm_filenames.append(dwdm_filename)
            channels.append(channel_number)

    for i, filename in enumerate(dwdm_filenames):
        file_path = DWDM_DIR / filename
        color = COLOURS[-i]  # -ve to avoid device transmission colors

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
            color=color,
            label=f"channel {int(channels[i])}",
        )

        # Fill with color under band-pass filter transmission
        fill_base = -50 * np.ones(datum["transmission"].size)
        ax.fill_between(
            x=datum["wavelength"],
            y1=datum["transmission"],
            y2=fill_base,
            alpha=0.25,
            color=color,
        )


if __name__ == "__main__":
    main()
