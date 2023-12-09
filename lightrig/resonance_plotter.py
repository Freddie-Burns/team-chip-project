import os
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


COLOURS = ['b', 'g', 'r', 'c', 'm', 'y']
DWDM_CHANNELS = (32, 33, 35)  # Channels to show transmission data
DWDM_DIR = Path("../data/dwdm")
RESONANCE_DIR = Path("../data/resonance")
Y_LIM = (-20,-17)

# Usually only plot one resonance file
# Can plot more than one to compare
# e.g. to see if resonances shift over time
FILES = [
    "ring-17 2023-12-01 10-49-28.csv",
]


def main():
    # Create matplotlib plot and set y-axis limits
    ax = plt.subplot()
    plt.ylim(Y_LIM)
    plot_channel_centers(ax)
    plot_transmission_data(ax)
    plot_dwdm_transmission(ax)
    plt.show()


def plot_channel_centers(ax):
    """Plot all DWDM channel central wavelengths as dotted lines."""
    channels = pd.read_csv(DWDM_DIR / "channel wavelength table.csv")
    for i in channels.index:
        wavelength = channels.iloc[i]["Wavelength"]
        channel = channels.iloc[i]["Channel"]
        ax.vlines(wavelength, *Y_LIM, 'k', ':')
        ax.text(wavelength+0.05, Y_LIM[0]+0.05, f"{int(channel)}", rotation=90)


def plot_transmission_data(ax):
    """Plot transmission against frequency for specified csv files."""
    file_paths = [RESONANCE_DIR / file for file in FILES]
    for file_path in file_paths:
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


def plot_dwdm_transmission(ax):
    """Plot transmission data for specified DWDM channels"""
    channel_number = None
    dwdm_filenames = []

    for dwdm_filename in os.listdir(DWDM_DIR):
        try: channel_number = int(dwdm_filename[8:10])
        except ValueError: pass
        if channel_number in DWDM_CHANNELS:
            dwdm_filenames.append(dwdm_filename)

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
