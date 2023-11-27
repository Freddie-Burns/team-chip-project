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

    def scan(self, wavelengths, save_path, device_name):
        """
        wavelengths:    numpy.array 1d
                        Frequencies laser will sweep.

        save_path:      pathlib.Path
                        Directory to save csv data file.

        device_name:    string
                        Name of tested device for file name.
        """
        # Switch on laser
        if self.laser is not None:
            try: self.laser.switch_on()
            except: raise Exception("No laser connection")

        transmission = np.zeros(wavelengths.shape)

        # Scan wavelengths and collect data
        for i, wavelength in enumerate(wavelengths):
            self.laser.set_wavelength(wavelength)
            self.powermeter.set_wavelength(wavelength)
            time.sleep(0.2) # time for laser to adjust and stabilise
            transmission[i] = self.powermeter.measure()

        # Write data to file
        data = np.stack((wavelengths, transmission), axis=1)
        file_path = save_path / f"{device_name}_{timestamp()}.csv"
        np.savetxt(file_path, data, delimiter=',')
