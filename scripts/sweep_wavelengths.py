"""
Script to run wavelength sweep once manually coupled.
"""

from pathlib import Path

from lightrig.laser import Laser
from lightrig.lightrig import LightRig
from lightrig.powermeter import Powermeter


# Define powermeter params
powermeter_serials = ['P0001012', 'P0000901']
powermeter_models = ['PM100D']
powermeter_units = ['dBm']
# NOTE this does not set the units on the PMs, it is intended for readout only

# Define driver params
m2_serial_port_name = "COM4"
# USB port for powermeter 'USB0::4883::32888::P0001012::0::INSTR'

# Define laser params
laser_com_port = 7
laser_channel = 1

local_optimisation_scan_range_um = 4
coupling_threshold_dB = -30
foldername = Path("../sweep_data")


if __name__ == '__main__':
    # ---------- Technology settings -------------

    laser = Laser(COM_port=laser_com_port, channel=laser_channel)
    powermeter = Powermeter()

    # ---------- Connect to LightRig -------------

    device = LightRig(
        m2_serial_port_name=m2_serial_port_name,
        pd_serials=powermeter_serials,
        pd_models=powermeter_models,
        units=powermeter_units,
        laser_port_name=laser_com_port,
        laser_channel=laser_channel
    )

    # Read in structure dictionary
    device.read_port_csv('device_coords_01.csv')

    # Run scan with additional settings
    device.scan(
        optimise_range_um=local_optimisation_scan_range_um,
        coupling_threshold_db=coupling_threshold_dB,
        foldername=foldername
    )
