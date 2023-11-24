from __future__ import print_function

import os

import pyvisa


class Laser(object):

	def __init__(self, **kwargs):

		self.laser_COM_port = 1
		self.channel = 1

		# Get arguments from init
		for para in ['laser_COM_port', 'channel']:
			try:
				self.__setattr__(para, kwargs[para])
			except KeyError:
				continue

		rm = pyvisa.ResourceManager('@py')

		if os.name == 'posix':
			self.laser = rm.open_resource(serial = '/dev/tty{:}'.format(self.laser_COM_port))
		else:
			# self.laser = rm.open_resource(serial = "ASRL{}::INSTR".format(self.laser_COM_port))
			self.laser = rm.open_resource(f"ASRL{self.laser_COM_port}::INSTR")
		self.laser.timeout = 20000
		self.laser.read_termination = '\r>'
		self.laser.write_termination = '\r'

		return

	def laser_enable(self):
		response = self.laser.query(f"CH{self.channel}:ENABLE").strip()
		if not response == f"CH{self.channel}:OK":
			raise Exception(f"Error: {response}")
		return

	def switch_on(self):
		response = self.laser.query("CH{:}:ENABLE".format(self.channel)).strip()
		if not response == "CH{:}:OK".format(self.channel):
			raise Exception("Error: {}".format(response))

		return

	def set_laser_wavelength(self, w = '1550'):

		self.laser_enable()

		# set laser wavelength
		response = self.laser.query("CH{:}:L={}".format(self.channel, w)).strip()
		if not response == "CH{:}:OK".format(self.channel):
			raise Exception("Error: {}".format(response))

		return
