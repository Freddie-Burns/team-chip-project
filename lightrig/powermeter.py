import math
import time

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

    def measure(self, channel=1):
        self.powermeter.query('READ?')
        result_w = float(self.powermeter.query('read?;*OPC?', delay=self.read_timeout).split(";")[0], )
        # result_w = float(self.instr.query('MEASURE:POWER?'))
        if math.isnan(result_w):
            return 10 * math.log(result_w * 1000, 10) # to dBm
        else:
            return float('nan')

    def set_wavelength(self, wl_nm):
        self.laser.write('sense:correction:wav {0}'.format(wl_nm))
        time.sleep(0.005)

    def get_wavelength(self):
        r = float(self.laser.query('sense:correction:wav?')) / 1e-9
        return r
