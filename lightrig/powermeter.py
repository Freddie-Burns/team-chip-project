from __future__ import print_function

import math
import os
import time
from collections import deque as fifo

import numpy as np
import pyvisa

from lightrig.errors import ERRORS


class Powermeter:
    """
	Class which handles Thorlabs powermeter setup, user interfacing, and data processing.

    model = None               Photodiode model e.g. 'PM100USB
	serial = None              Photodiode serial e.g. 'PM000192
	unit = None         	   Unit settings {'W', 'mW', 'dBm'}
	wavelength = None          Central wavelength [nm]
	average = 10  			   Number of measurements to average over [int]
	read_timeout = 0.5         Readout cut off time [s]

	log = fifo(maxlen = 256)   Log FIFO of communications
	log_handler = None         Function which catches log dictionaries
	log_to_stdout = True       Copy new log entries to stdout
	"""
    def __init__(self, *args, **kwargs):
        # Defaults
        self.model = "PM100D"
        self.serial = None  # Name of serial port, eg 'COM1' or '/dev/tty1'
        self.unit = 'dBm'  # {'W', 'mW', 'dBm'}
        self.wavelength = 1550  # Wavelength in nm
        self.averages = 10  # Measurement averages
        self.read_timeout = 0.5  # Read timeout (s)

        self.log = fifo(maxlen=256)  # Log FIFO of communications
        self.log_handler = None  # Function which catches log dictionaries
        self.log_to_stdout = True  # Copy new log entries to stdout
        self.init_time = time.time()
        self.instr = None

        # Get arguments from init
        # Populate parameters, if provided
        for para in ['model', 'serial', 'unit', 'wavelength', 'averages',
                     'read_timeout', 'log_to_stdout']:
            try:
                self.__setattr__(para, kwargs[para])
            except KeyError:
                continue

        if self.unit not in ['W', 'dBm', 'mW']:
            self.log_append(type='err', id=202)

        # For
        rm = pyvisa.ResourceManager('@py')
        resources = rm.list_resources()

        pm_serial = None
        instrs = []

        for r in resources:
            if self.serial in r.split('::'):
                pm_serial = r
                self.instr = rm.open_resource(pm_serial, read_termination='\n')
                print('Resource is {:}'.format(pm_serial))

        # Throw error if connection failed
        if self.instr is None:
            self.log_append(type='err', id=201)

    def measure(self, channel=1):
        self.instr.query('READ?')
        result_w = float(self.instr.query('read?;*OPC?',delay=self.read_timeout).split(";")[0],)
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
