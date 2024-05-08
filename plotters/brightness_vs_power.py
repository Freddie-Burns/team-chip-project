from pathlib import Path
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns

from plotters.helpers.utils import calculate_brightness


sns.set()


DATA_DIR = Path("../data/swabian/coincidences")
FILES = [
    "ring-12 binwidth_10ps trigger_0.07V power_1dBm integration_120s "
    "2023-12-13 11-22-28.csv",
    "ring-12 binwidth_10ps trigger_0.07V power_2dBm integration_120s "
    "2023-12-13 11-15-32.csv",
    "ring-12 binwidth_10ps trigger_0.07V power_3dBm integration_120s "
    "2023-12-13 11-12-05.csv",
    "ring-12 binwidth_10ps trigger_0.07V power_4dBm integration_120s "
    "2023-12-13 11-09-40.csv",
    "ring-12 binwidth_10ps trigger_0.07V power_5dBm integration_120s "
    "2023-12-13 11-07-15.csv",
    "ring-12 binwidth_10ps trigger_0.07V power_6dBm integration_120s "
    "2023-12-13 11-04-50.csv",
    "ring-12 binwidth_10ps trigger_0.07V power_7dBm integration_180s "
    "2023-12-13 10-57-31.csv",
]

times = [120, 120, 120, 120, 120, 120, 180]
powers = [1, 2, 3, 4, 5, 6, 7]
brightnesses = []
for i, file in enumerate(FILES):
    filepath = DATA_DIR / file
    time = times[i]
    power = powers[i]
    brightnesses.append(calculate_brightness(filepath, time, power))

mean_brightness = np.mean(brightnesses)
std_brightness = np.std(brightnesses)

fig, ax = plt.subplots()
plt.scatter(powers, brightnesses, marker='x')
plt.xlabel("power (dBm)")
plt.ylabel("brightness (pairs / s / mW^2)")
plt.title("Ring 12 brightness vs pump power")

# Place textbox with mean and std
textstr = '\n'.join((
    f'$\mu={mean_brightness:.1f}$',
    f'$\sigma={std_brightness:.1f}$',
))
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax.text(0.05, 0.05, textstr, transform=ax.transAxes, fontsize=14,
        verticalalignment='bottom', bbox=props)

plt.savefig(r"figures/brightness_vs_power.png")
plt.show()
