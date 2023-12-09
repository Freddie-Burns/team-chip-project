import math
import time

import numpy as np
import pyvisa


class Powermeter:
    """
	Class which handles Thorlabs powermeter setup and user interfacing.

	serial = None              Photodiode serial e.g. 'PM000192
	"""
    def __init__(self, serial="P0001012"):
        # Defaults
        self.model = "PM100D"
        self.serial = serial
        self.unit = "dBm"

        rm = pyvisa.ResourceManager('@py')
        resources = rm.list_resources()

        for resource in resources:
            if self.serial in resource:
                self.powermeter = rm.open_resource(
                    resource, read_termination='\n')
                print(f"Powermeter is {resource}")

    def measure(self):
        """
        Read power, convert Watts to dBm, return value.
        """
        try:
            result_w = float(self.powermeter.query('measure:power?'))
            return 10 * math.log(result_w * 1000, 10) # to dBm
        except:
            return np.NaN

    def set_wavelength(self, wl_nm):
        self.powermeter.write(f"sense:correction:wav {wl_nm}")
        time.sleep(0.01)

    def get_wavelength(self):
        r = float(self.powermeter.query('sense:correction:wav?')) / 1e-9
        return r
