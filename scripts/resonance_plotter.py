from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

src_dir = Path(__file__).parents[1]
sweep_dir = src_dir / "sweep_data"
file_path_1 = sweep_dir / "ring-04-dwdm 2023-12-04 14-58-11.csv"
file_path_2 = sweep_dir / "ring-04-dwdm 2023-12-04 15-00-33.csv"

sweep_data_1 = pd.read_csv(file_path_1, header=None, names=["wavelength", "transmission"])
sweep_data_2 = pd.read_csv(file_path_2, header=None, names=["wavelength", "transmission"])

ax = sweep_data_1.plot(kind='line', x="wavelength", y="transmission")
sweep_data_2.plot(kind='line', x="wavelength", y="transmission", ax=ax)

plt.show()
