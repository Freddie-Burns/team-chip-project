from matplotlib import pyplot as plt
from helpers import resonance


channel_centres = range(29, 41)
files = ["ring-01 2023-12-04 13-50-17.csv", "ring-24 2023-12-12 09-27-44.csv"]
labels = ["ring-01", "ring-24"]
xlim = (1545, 1554.5)
ylim = (-20.5, -17)


plt.figure()
ax = plt.subplot()
resonance.plot_channel_centers(ax, channel_centres, ylim)
resonance.plot_transmission_data(ax, files, labels)
plt.ylim(ylim)
plt.xlim(xlim)
plt.xlabel("wavelength / nm")
plt.ylabel("transmission / dB")
plt.savefig("figures/fsr_comparison.png")
plt.show()
