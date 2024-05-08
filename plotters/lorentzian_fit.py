from pathlib import Path
from matplotlib import pyplot as plt
from q_factors import fit_lorentzian

SRC_DIR = Path(__file__).parents[1]
RESONANCE_DIR = SRC_DIR / "data" / "resonance"
# FILE = "ring-15 2023-12-01 10-27-48.csv"
# PEAK = 1543
FILE = "ring-12 2023-12-13 10-04-47.csv"
PEAK = 1547.5

file_path = RESONANCE_DIR / FILE
fit_lorentzian(file_path, PEAK, plot=True)
plt.title("Lorentzian fitted to ring 12 transmission spectrum")
plt.savefig("figures/lorentzian_fit")
plt.show()
