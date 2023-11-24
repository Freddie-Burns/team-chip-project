from __future__ import print_function

import math
import os
import time
from collections import deque as fifo

import numpy as np
import pyvisa

from lightrig.errors import ERRORS


class Powermeter(object):
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
        """
		Initialiser.
		"""

        # Defaults
        self.model = None  # Device model, supported 'N7747A; PM100D; PM100USB'
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
        if os.name == 'posix':
            self.instr.query('READ?')
            result_w = float(
                self.instr.query(
                    'read?;*OPC?',
                    delay=self.read_timeout).split(";")[0],
            )

            if math.isnan(result_w):
                result_w = 0.
            if self.unit == 'W':
                return result_w
            elif self.unit == 'mW':
                return result_w * 1000
            elif self.unit == 'dBm':
                return (10 * math.log(result_w * 1000,
                                      10)) if result_w > 0 else float('nan')

        else:
            if (self.model == 'PM100D' or self.model == 'PM100USB'):
                result_w = float(self.instr.query('MEASure:POWer?'))
            elif self.model == 'N7747A':
                if channel not in [1, 2]:
                    raise AttributeError(
                        'Channel number for model {0} must be in [1,2]. Specified channel {1} is invalid.'.format(
                            self.model, channel))
                result_w = float(
                    self.instr.query('read{ch}:pow?'.format(ch=channel),
                                     delay=self.read_timeout))
            else:
                raise AttributeError('Unknown model "{0}".'.format(self.model))

            if math.isnan(result_w):
                result_w = 0.

            if self.unit == 'W':
                return result_w
            elif self.unit == 'mW':
                return result_w * 1000
            elif self.unit == 'dBm':
                return (10 * math.log(result_w * 1000,
                                      10)) if result_w > 0 else float('nan')

    def set_wavelength(self, wl_nm):
        self.laser.write('sense:correction:wav {0}'.format(wl_nm))
        time.sleep(0.005)

    def get_wavelength(self):
        r = float(self.laser.query('sense:correction:wav?')) / 1e-9
        return r

    def set_averages(self, n_averages):
        self.laser.write('sens:aver {0}'.format(n_averages))
        time.sleep(0.005)

    def get_statistics(self, n_counts=100, channel=1):
        data = []
        for _ in range(n_counts):
            power = self.measure(channel=channel)
            if not math.isnan(power):
                data.append(power)
            else:
                return {"mean": math.nan, "stdev": math.nan, "data": []}
            time.sleep(0.05)
        if data:
            mean = sum(data) / len(data)
            stats = {
                "min": min(data),
                "max": max(data),
                "mean": mean,
                "stdev": np.std(np.array(data), axis=0),
                "data": data
            }
            return stats
        else:
            # only works in dBm for now set to noise floor if NaN
            stats = {
                "min": -120.0,
                "max": -120.0,
                "mean": -120.0,
                "stdev": 0.0,
                "data": []
            }
            return stats

    def log_append(self, type='err', id=''):
        """
		Log an event; add both a calendar- and process-timestamp.
		"""
        # Append to log fifo
        self.log.append({'timestamp': time.asctime(),
                         'process_time': round(time.time() - self.init_time, 3),
                         'type': type, 'id': int(id)})
        # Send to handler function (if defined)
        if self.log_handler is not None:
            self.log_handler(self.log[-1])
        # Send to stdout (if requested)
        if self.log_to_stdout:
            self.print_log(n=1)

    def print_log(self, n=None):
        """
		Print the n last log entries. If n == None, print all log entries.
		"""
        if n is None:
            n = len(self.log)

        for i in range(-n, 0):
            print('@ {0: 8.1f} ms, {1} : {2}'.format(
                1000 * self.log[i]['process_time'], self.log[i]['type'],
                self.log[i]['id']) + ' ' + ERRORS[int(self.log[i]['id'])])
