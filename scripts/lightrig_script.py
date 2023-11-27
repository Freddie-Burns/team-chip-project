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
device.sweep(
    optimise_range_um=local_optimisation_scan_range_um,
    coupling_threshold_db=coupling_threshold_dB,
    foldername=foldername
)
