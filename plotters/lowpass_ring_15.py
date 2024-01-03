from pathlib import Path

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

from helpers.lowpass import lowpass


sns.set()


FILE = "ring-15 2023-12-01 10-27-48.csv"
LOOP = False
PERIOD = 20
SRC_DIR = Path(__file__).parents[1]
RESONANCE_DIR = SRC_DIR / "data" / "resonance"


datum = pd.read_csv(
    RESONANCE_DIR / FILE,
    header=None,
    names=["wavelength", "transmission"],
)
wavelength = np.array(datum["wavelength"])[-500:]
transmission = np.array(datum["transmission"])[-500:]
plt.plot(wavelength, transmission, label="original")

if LOOP:
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
plt.savefig("figures/lowpass_ring_15.png")
plt.show()
