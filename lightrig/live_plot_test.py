from time import sleep

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


# Collect data to plot
DATA_PATH = r"C:\Users\fredd\PycharmProjects\team-chip-project\data" \
            r"\resonance\ring-17 2023-12-01 10-49-28.csv"
PREPARED_DATA = pd.read_csv(
    DATA_PATH,
    header=None,
    names=["wavelength", "transmission"],
)

# Number of wavelengths in the sweep
start = 1545
end = 1555
step = 0.02
sweep_size = int((end - start) / step) + 1

# Initialise arrays to hold data
wavelengths = np.linspace(start, end, sweep_size)
transmission = np.empty(wavelengths.shape)
transmission[:] = np.nan

# Create plot
ax = plt.subplot()
plt.xlim(wavelengths[0], wavelengths[-1])
plt.show(block=False)
ax.plot(wavelengths, transmission)
plt.title("Transmission Power", fontsize=20)
plt.xlabel("wavelength / nm")
plt.ylabel("transmission / uW")

# Scan wavelengths and collect data
for i, wavelength in enumerate(PREPARED_DATA["wavelength"]):
    transmission[i] = PREPARED_DATA.iloc[i]["transmission"]
    plt.pause(0.01)
    ax.clear()
    ax.plot(wavelengths, transmission)
    plt.xlim(wavelengths[0], wavelengths[-1])
    plt.title("Transmission Power", fontsize=20)
    plt.xlabel("wavelength / nm")
    plt.ylabel("transmission / dBm")

plt.show()
