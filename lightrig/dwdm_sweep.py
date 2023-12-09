"""
Script to run wavelength sweep once manually coupled.
Saves swabian as a csv file in specified directory.
"""

from pathlib import Path

from instruments import Laser
from instruments import Powermeter
from instruments import Sweeper


# Wavelength sweep parameters
device_name = "channel-39"
centre_wavelength = 1546
start_wavelength = centre_wavelength - 1
end_wavelength = centre_wavelength + 1
wavelength_step = 0.1

# Instrument parameters
powermeter_serial = 'P0001012'
laser_com_port = 7
laser_channel = 1
save_path = Path("../data/dwdm")

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
