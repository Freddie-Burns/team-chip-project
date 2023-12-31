from pathlib import Path

from matplotlib import pyplot as plt

from helpers import resonance


channel_centres = range(29, 41)
dwdm_channels = (30, 33, 35, 37, 40)
files = ["ring-12 2023-12-13 10-04-47.csv"]
labels = ["ring-12"]
xlim = (1545, 1554.5)
ylim = (-15, -11)


plt.figure()
ax = plt.subplot()
resonance.plot_channel_centers(ax, channel_centres)
resonance.plot_transmission_data(ax, files, labels)
resonance.plot_dwdm_transmission(ax, dwdm_channels)
plt.ylim(ylim)
plt.xlim(xlim)
plt.xlabel("wavelength / nm")
plt.ylabel("transmission / dB")
plt.savefig("figures/ring_12_resonances.png")
plt.show()
