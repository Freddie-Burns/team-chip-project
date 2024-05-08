from pathlib import Path
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy.interpolate import griddata
import numpy as np
import pandas as pd
import seaborn as sns

from helpers import resonance, lowpass


sns.set()


SRC_DIR = Path(__file__).parents[1]
RESONANCE_DIR = SRC_DIR / "data" / "resonance"
LOWPASS = False
FILES = {
    1: "ring-01 2023-11-29 14-00-44.csv",
    3: "ring-03 2023-11-29 14-38-44.csv",
    4: "ring-04 2023-12-04 14-17-28.csv",
    5: "ring-05 2023-12-01 10-14-03.csv",
    7: "ring-07 2023-11-29 15-10-31.csv",
    9: "ring-09 2023-11-29 15-24-33.csv",
    11: "ring-11 2023-11-29 15-39-01.csv",
    12: "ring-12 2023-12-13 10-04-47.csv",
    13: "ring-13 2023-11-29 15-53-45.csv",
    15: "ring-15 2023-12-01 10-27-48.csv",
    16: "ring-16 2023-12-12 10-26-18.csv",
    # 17: "ring-17 2023-12-01 10-49-28.csv",
    # 24: "ring-24 2023-12-12 09-27-44.csv",
}
PEAK_WAVELENGTHS = {
    1: [1545.8, 1550.8,],
    3: [1550.4, 1555.3,],
    4: [1548.2,],
    5: [1544.8, 1547.6, 1550.2, 1553, 1555.7, 1558.5],
    7: [1547, 1549.8, 1552.5, 1555.3, 1558, 1560.8, 1563.6],
    9: [1542.1, 1545.8, 1549.6, 1551.4, 1553.4, 1555.3, 1557.2],
    11: [1542, 1543.9, 1545.7, 1547.6, 1551.4, 1553.3, 1555.2, 1557, 1559],
    12: [1545.6, 1547.5, 1549.4, 1551.2, 1553.1],
    13: [1543.6, 1545, 1547.9, 1549.3, 1552.2, 1553.7, 1555.1, 1558, 1559.5],
    15: [1541.6, 1543, 1544.5, 1545.9, 1547.3, 1548.8, 1550.2, 1551.7,
         1553.1, 1554.6, 1556, 1557.5, 1559],
    16: [1546.5, 1547.9, 1549.4, 1550.8, 1552.3, 1553.7],
    # 17: [1549.6,],
    # 24: [1547.7,],
}
# Radius, gap, textbox coords
RING_DATA = {
    1: [0.251, 21, (0.05, 0.05)],
    3: [0.28, 21, (0.54, 0.05)],
    4: [0.299, 21, (0.92, 0.05)],
    5: [0.251, 36, (0.05, 0.25)],
    7: [0.28, 36, (0.54, 0.25)],
    9: [0.251, 52, (0.05, 0.58)],
    11: [0.28, 52, (0.51, 0.58)],
    12: [0.299, 52, (0.89, 0.58)],
    13: [0.251, 67, (0.05, 0.9)],
    15: [0.28, 67, (0.51, 0.9)],
    16: [0.299, 67, (0.89, 0.9)],
}


def main():
    # plot_full_transmission(FILES.values())
    # plt.show()
    plot_mean_q_factors()


def plot_mean_q_factors(scatter=True):
    ax = plt.subplot()
    mean_q_factors = {}
    for ring, file in FILES.items():
        peaks = PEAK_WAVELENGTHS[ring]
        file_path = RESONANCE_DIR / file
        q_factors = []
        for peak in peaks:
            q = fit_lorentzian(file_path, peak, plot=False, filt=LOWPASS)
            q_factors.append(q)
        mean_q_factors[ring] = np.mean(q_factors)
    q_factor_heatmap(mean_q_factors)

    if scatter:
        # Scatter plot ring labels
        labels = []
        gaps = []
        radii = []
        box_coords = []
        for ring, coords in RING_DATA.items():
            labels.append(str(ring))
            gaps.append(coords[0])
            radii.append(coords[1])
            box_coords.append(coords[2])
        plt.scatter(gaps, radii, color='wheat', marker='o')
        plt.scatter(gaps, radii, marker='x')

        for i, label in enumerate(labels):
            print(label)
            props = dict(boxstyle='round', facecolor='wheat')
            ax.text(
                # gaps[i],
                # radii[i],
                *box_coords[i],
                label,
                transform=ax.transAxes,
                fontsize=14,
                verticalalignment='bottom',
                bbox=props
            )

    if LOWPASS:
        plt.savefig("figures/q_factor_heatmap_lowpass.png")
    elif scatter:
        plt.savefig("figures/q_factor_heatmap_labeled.png")
    else:
        plt.savefig("figures/q_factor_heatmap.png")

    plt.show()


def q_factor_heatmap(q_factors: dict):
    file_path = SRC_DIR / "data" / "device_coords" / "device_params.csv"
    params = pd.read_csv(file_path, index_col="Device")
    params.insert(2, "Q Factor", np.NAN, True)
    for ring, q_factor in q_factors.items():
        params.at[ring, "Q Factor"] = round(q_factor)
    params = params.dropna()
    print(params)
    x = np.array(params["Gap"])
    y = np.array(params["Radius"])
    z = np.array(params["Q Factor"])

    print("Highest Q factor:", max(z))

    X, Y = np.meshgrid(
        np.linspace(np.min(x), np.max(x), 20),
        np.linspace(np.min(y), np.max(y), 20)
    )

    interpolated_vals = griddata((x, y), z, (X, Y), method='cubic')
    plt.contourf(X, Y, interpolated_vals, levels=100)
    plt.colorbar()
    plt.xlabel(r"gap / $\mu$m")
    plt.ylabel(r"radius / $\mu$m")
    plt.title("Ring resonator Q factor")


def plot_lorentzian(file, mu):
    file_path = RESONANCE_DIR / file
    fit_lorentzian(file_path, mu)


def plot_full_transmission(files):
    for file in files:
        plt.figure()
        ax = plt.subplot()
        resonance.plot_transmission_data(ax, [file], [""])
        plt.title(file)
    # plt.ylim(ylim)
    # plt.xlim(xlim)
    plt.xlabel("wavelength / nm")
    plt.ylabel("transmission / dB")


def lorentzian(x, a, mu, lam, c):
    """Function for scipy.curve_fit to fit data to."""
    return a * lam / (((x - mu) ** 2) + lam ** 2) + c


def fit_lorentzian(filepath, mu, fsr=0.5, plot=False, filt=False):
    """
    Given approximate centre and assymptote of the Lorentzian
    return the q-factor.
    """
    datum = pd.read_csv(
        filepath,
        header=None,
        names=["wavelength", "transmission"],
    )

    wavelength = np.array(datum["wavelength"])
    transmission = np.array(datum["transmission"])

    if filt:
        transmission = lowpass.filter_transmission(transmission)

    mask = abs(wavelength - mu) < fsr
    wavelength = wavelength[mask]
    transmission = transmission[mask]

    # Fit Lorentzian to data
    a = min(transmission) - max(transmission)
    lam = 0.03
    c = max(transmission)
    guess = (a, mu, lam, c)
    popt, pcov = curve_fit(lorentzian, wavelength, transmission, guess)
    a, mu, lam, c = popt

    if plot:
        plt.figure()
        plt.scatter(wavelength, transmission, color='k', marker='x')

        # Upsample wavelengths for plotting Lorentzian
        wavelength = np.linspace(min(wavelength), max(wavelength), 1001)
        lorentzian_fit = lorentzian(wavelength, a, mu, lam, c)
        plt.plot(wavelength, lorentzian_fit, label="Lorentzian fit")
        plt.legend(loc="lower left")
        plt.xlabel("wavelength / nm")
        plt.ylabel("transmission / dB")

    q_factor = mu / lam
    print(q_factor)
    return q_factor


if __name__ == "__main__":
    main()
