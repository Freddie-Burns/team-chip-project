import os
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


COLOURS = ['b', 'g', 'r', 'c', 'm', 'y']

SRC_DIR = Path(__file__).parents[2]
DWDM_DIR = SRC_DIR / "data" / "dwdm"
RESONANCE_DIR = SRC_DIR / "data" / "resonance"

X_LIM = (1545, 1555)
Y_LIM = (-15, -11)


def main():
    channels = (30, 33, 35, 37, 40)  # channels to show transmission data

    # Usually only plot one resonance file
    # Can plot more than one to compare
    # e.g. to see if resonances shift over time
    files = ["ring-12 2023-12-13 10-04-47.csv", ]

    # Create matplotlib plot and set y-axis limits
    ax = plt.subplot()
    plt.ylim(Y_LIM)
    plt.xlim(X_LIM)
    plot_channel_centers(ax)
    plot_transmission_data(ax, files, "ring-12")
    plot_dwdm_transmission(ax, channels)
    plt.show()


def plot_channel_centers(ax, channels=range(51)):
    """Plot all DWDM channel central wavelengths as dotted lines."""
    print(os.listdir(DWDM_DIR))
    channel_data = pd.read_csv(DWDM_DIR / "channel_wavelength_table.csv")
    for i in channel_data.index:
        wavelength = channel_data.iloc[i]["wavelength"]
        channel = channel_data.iloc[i]["channel"]
        if channel not in channels: continue  # Don't include this channel
        ax.vlines(wavelength, *Y_LIM, 'k', ':')
        ax.text(wavelength-0.1, Y_LIM[1]+0.1, f"{int(channel)}", rotation=90)


def plot_transmission_data(ax, files, labels):
    """Plot transmission against frequency for specified csv files."""
    data = []
    for file in files:
        datum = pd.read_csv(
            RESONANCE_DIR / file,
            header=None,
            names=["wavelength", "transmission"],
        )
        data.append(datum)

    # Find the highest transmission
    # Adjust all sweeps to this for easier comparison
    if len(files) > 1:
        maxima = []
        for datum in data:
            maxima.append(datum["transmission"].max())
        max_transmission = max(maxima)
        for datum in data:
            diff = max_transmission - datum["transmission"].max()
            datum["transmission"] += diff

    # Plot adjusted transmission data
    for i, datum in enumerate(data):
        datum.plot(
            kind='line',
            x="wavelength",
            y="transmission",
            ax=ax,
            label=labels[i]  # Remove .csv from label
        )


def plot_fourier_transform(file):
    datum = pd.read_csv(
        RESONANCE_DIR / file,
        header=None,
        names=["wavelength", "transmission"],
    )
    transmission = np.array(datum["transmission"])
    n_points = len(transmission) // 2
    fft = np.fft.fft(transmission)
    fft[0] = fft[40:61] = fft[440:460] = 0
    plt.figure()
    plt.plot(abs(fft))
    original = np.fft.ifft(fft)
    plt.figure()
    plt.plot(original)


def plot_dwdm_transmission(ax, channels):
    """Plot transmission data for specified DWDM channels"""
    dwdm_filenames = []

    for dwdm_filename in os.listdir(DWDM_DIR):
        try:
            channel = int(dwdm_filename[8:10])
            if channel in channels:
                dwdm_filenames.append(dwdm_filename)
        except ValueError:
            pass  # Some files will not have a channel number

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
