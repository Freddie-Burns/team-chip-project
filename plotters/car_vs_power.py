from pathlib import Path
from matplotlib import pyplot as plt
import seaborn as sns

from plotters.helpers.utils import calculate_car


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


powers = [1, 2, 3, 4, 5, 6, 7]
cars = []
for file in FILES:
    filepath = DATA_DIR / file
    cars.append(calculate_car(filepath))

print("Highest CAR", max(cars))

plt.scatter(powers, cars, marker='x')
plt.xlabel("power / dBm")
plt.ylabel("CAR")
plt.title("Ring 12 CAR vs power")
plt.savefig(r"figures/car_vs_power.png")
plt.show()
