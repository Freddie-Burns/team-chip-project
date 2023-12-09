"""
Script to run wavelength sweep once manually coupled.
Saves data as a csv file in specified directory.
"""

from pathlib import Path

from lightrig.laser import Laser
from lightrig.powermeter import Powermeter
from lightrig.sweeper import Sweeper


# Wavelength sweep parameters
device_name = "ring-04-dwdm"
start_wavelength = 1553
end_wavelength = 1554
wavelength_step = 0.01

# Instrument parameters
powermeter_serial = 'P0001012'
laser_com_port = 7
laser_channel = 1
save_path = Path("../data/resonance")

# Connect to instruments
laser = Laser(COM_port=laser_com_port, channel=laser_channel)
powermeter = Powermeter(powermeter_serial)

# Run wavelength sweep
sweeper = Sweeper(laser, powermeter)
sweeper.sweep(
    save_path=save_path,
    device_name=device_name,
    start=start_wavelength,
    end=end_wavelength,
    step=wavelength_step,
)
