import os
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

src_dir = Path(__file__).parents[1]
dwdm_dir = src_dir / "dwdm_sweep"

sweep_data = []

for file in os.listdir(dwdm_dir):
    sweep_data.append(pd.read_csv(dwdm_dir / file, header=None, names=["wavelength", "transmission"]))

sweep_data_0 = sweep_data[0]
ax = sweep_data_0.plot(kind='line', x="wavelength", y="transmission", ylim=(-20, 0))
for datum in sweep_data[1:]:
    datum.plot(kind='line', x="wavelength", y="transmission", ax=ax, ylim=(-20, 0))

plt.show()
