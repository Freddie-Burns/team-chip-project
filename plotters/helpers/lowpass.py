from pathlib import Path

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from scipy.signal import butter, sosfiltfilt


sns.set()


FILE = "ring-15 2023-12-01 10-27-48.csv"
PERIOD = 20
SRC_DIR = Path(__file__).parents[2]
RESONANCE_DIR = SRC_DIR / "data" / "resonance"


def find_high_frequency_fft():
    file = "ring-01 2023-11-29 14-00-44.csv"
    datum = pd.read_csv(
        RESONANCE_DIR / file,
        header=None,
        names=["wavelength", "transmission"],
    )
    transmission = np.array(datum["transmission"])
    ax = plt.subplot()
    plt.plot(transmission)
    noise_fft = np.fft.fft(transmission[300:500])  # No dip in this slice
    plt.figure()
    plt.plot(abs(noise_fft[1:]))
    # original = np.fft.ifft(fft)
    # ax.plot(original)
    plt.show()


def lowpass(data: np.ndarray, cutoff: float, poles: int = 5):
    sos = butter(poles, cutoff, 'lowpass', fs=len(data), output='sos')
    filtered_data = sosfiltfilt(sos, data)
    return filtered_data


def plot_filtered(file, loop=False):
    datum = pd.read_csv(
        RESONANCE_DIR / file,
        header=None,
        names=["wavelength", "transmission"],
    )
    wavelength = np.array(datum["wavelength"])[-500:]
    transmission = np.array(datum["transmission"])[-500:]
    plt.plot(wavelength, transmission, label="original")

    if loop:
        for period in range(20, 30, 2):
            cutoff = len(transmission) // period
            filtered = lowpass(transmission, cutoff)
            plt.plot(filtered, label=period)

    else:
        cutoff = len(transmission) // PERIOD
        filtered = lowpass(transmission, cutoff)

    plt.plot(wavelength, filtered, 'k--', label="filtered")
    plt.legend()
    plt.xlabel("wavelength / nm")
    plt.ylabel("transmission / dB")
    plt.title("Ring 15 low-pass filter transmission spectrum")
    plt.savefig("lowpass_ring_15.png")
    plt.show()


def filter_transmission_file(file):
    datum = pd.read_csv(
        RESONANCE_DIR / file,
        header=None,
        names=["wavelength", "transmission"],
    )
    transmission = np.array(datum["transmission"])
    cutoff = len(transmission) // PERIOD
    return lowpass(transmission, cutoff)


def filter_transmission(transmission, period=None):
    if period is None:
        period = PERIOD
    cutoff = len(transmission) // period
    return lowpass(transmission, cutoff)


def plot_fourier_transform(file):
    datum = pd.read_csv(
        RESONANCE_DIR / file,
        header=None,
        names=["wavelength", "transmission"],
    )
    transmission = np.array(datum["transmission"])
    ax = plt.subplot()
    plt.plot(transmission)
    fft = np.fft.fft(transmission)
    cutoff = len(fft) // PERIOD
    plt.figure()
    plt.plot(abs(fft[1:]))
    fft[cutoff:-cutoff] = 0
    plt.plot(abs(fft[1:]))
    original = np.fft.ifft(fft)
    ax.plot(original)
    plt.show()


if __name__ == "__main__":
    # plot_fourier_transform(FILE)
    # find_high_frequency_fft()
    plot_filtered(FILE)
