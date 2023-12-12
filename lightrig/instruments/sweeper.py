"""
Module for sweeping laser frequencies into a device and measuring
corresponding power output.
"""

import datetime
import time
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .laser import Laser
from .powermeter import Powermeter


DWDM_FILE = Path("../data/dwdm") / "channel_wavelength_table.csv"


def timestamp():
    """Time stamping for swabian save"""
    return datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')


class Sweeper:
    def __init__(self, laser: Laser, powermeter: Powermeter):
        self.laser = laser
        self.powermeter = powermeter

    def sweep(self, save_path, device_name, start=1540, end=1570, step=0.1):
        """
        start:          int, float
                        Initial wavelength of sweep in nm.

        end:            int, float
                        Final wavelength of sweep in nm.

        step:           int, float
                        Increment between each wavelength in sweep in nm.

        save_path:      pathlib.Path
                        Directory to save csv swabian file.

        device_name:    string
                        Name of tested device for file name.
        """
        # Switch on laser
        try: self.laser.switch_on()
        except: raise Exception("No laser connection")

        # Number of wavelengths in the sweep
        sweep_size = int((end - start) / step) + 1

        # Initialise arrays to hold data
        wavelengths = np.linspace(start, end, sweep_size)
        transmission = np.empty(wavelengths.shape)
        transmission[:] = np.nan

        # Drop DWDM channels outside plotting range
        all_channels = pd.read_csv(DWDM_FILE)
        visible_channels = []
        for i in all_channels.index:
            channel = all_channels.iloc[i]["channel"]
            centre = all_channels.iloc[i]["wavelength"]
            if (wavelengths[0] < centre) and (centre < wavelengths[-1]):
                visible_channels.append((channel, centre))

        # Create plot
        ax = plt.subplot()
        plt.xlim(wavelengths[0], wavelengths[-1])
        plt.show(block=False)
        ax.plot(wavelengths, transmission)

        # Scan wavelengths and collect data
        for i, wavelength in enumerate(wavelengths):
            self.laser.set_wavelength(wavelength)
            time.sleep(0.2)  # time for laser to adjust and stabilise
            transmission[i] = self.powermeter.measure()

            # Update graph
            plt.pause(0.01)
            ax.clear()
            plt.xlim(wavelengths[0], wavelengths[-1])
            ax.plot(wavelengths, transmission)
            y_lim = ax.get_ylim()

            for channel, channel_wavelength in visible_channels:
                ax.vlines(channel_wavelength, *y_lim, 'k', ':')
                position = (channel_wavelength + 0.05, y_lim[0])
                label = f"{int(channel)}"
                ax.text(*position, label, rotation=90)

        # Combine wavelengths and power into 2 x n array then save
        data = np.stack((wavelengths, transmission), axis=1)
        file_path = save_path / f"{device_name} {timestamp()}.csv"
        np.savetxt(file_path, data, delimiter=',')

        # plt.plot(wavelengths, transmission)
        plt.title("Transmission Power", fontsize=20)
        plt.xlabel("wavelength / nm")
        plt.ylabel("transmission / dBm")
        plt.show()
