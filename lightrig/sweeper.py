"""
Module for sweeping laser frequencies into a device and measuring
corresponding power output.
"""

import datetime
import time

import numpy as np

from laser import Laser
from powermeter import Powermeter


def timestamp():
    """Time stamping for data save"""
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
                        Directory to save csv data file.

        device_name:    string
                        Name of tested device for file name.
        """
        # Switch on laser
        if self.laser is not None:
            try: self.laser.switch_on()
            except: raise Exception("No laser connection")

        # Number of wavelengths in the sweep
        sweep_size = int((end - start) / step) + 1

        # Initialise arrays to hold data
        wavelengths = np.linspace(start, end, sweep_size)
        transmission = np.zeros(wavelengths.shape)

        # Scan wavelengths and collect data
        for i, wavelength in enumerate(wavelengths):
            self.laser.set_wavelength(wavelength)
            self.powermeter.set_wavelength(wavelength)
            time.sleep(0.2) # time for laser to adjust and stabilise
            transmission[i] = self.powermeter.measure()

        # Combine wavelengths and power into 2 x n array then save.
        data = np.stack((wavelengths, transmission), axis=1)
        file_path = save_path / f"{device_name}_{timestamp()}.csv"
        np.savetxt(file_path, data, delimiter=',')
