"""
Error codes for lightrig control.
"""

# Errors realting to the driver, as defined by Qontrol Systems
QONTROL_ERRORS = {
    0: 'Unknown error.',
    3: 'Power error.',
    4: 'Calibration error.',
    5: 'Output error.',
    10: 'Unrecognised command.',
    11: 'Unrecognised input parameter.',
    12: 'Unrecognised channel.',
    13: 'Operation forbidden.',
    14: 'Serial buffer overflow.',
    15: 'Serial communication error.',
    16: 'Command timed out.',
    17: 'SPI error.',
    18: 'ADC error.',
    19: 'I2C error.',
    30: 'Too many errors, some have been suppressed.',
    31: 'Firmware trap.',
    90: 'Powered up.',
    1: 'Out-of-range error.',
    20: 'Interlock triggered.'}

# Additional errors relating to automated scanning
LTP_ERRORS = {
    110: 'Incorrect device CSV format',
    111: 'Not enough powermeters connected to perform measurement',
    112: 'Powermeter(s) failed to connect',
    113: 'Attempting to run scan with no device dictionary',
    114: 'Device out of scan range',
    115: 'Local optimisation scan range must be greater than 3.175 um',
    116: 'Not enough powermeter connected to complete scan',
    117: 'Laser connection failed',
    118: 'Laser throwing error during turn on'}
# ...}

LTP_WARNINGS = {
    401: 'Ensure you are couple into device 1 as defined in line 1 of your '
         'device dictionary.',
    402: 'Ensure M2 channel 0 = X, 1 = Y, Z = 2'}
# ...}

THOR_ERRORS = {
    201: 'Powermeter not found, connection error!',
    202: 'Specified unit not recognised'
}

ERRORS = {**QONTROL_ERRORS, **LTP_ERRORS, **LTP_WARNINGS, **THOR_ERRORS}

# Define fatal errors
fatal_errors = [0, 1, 20, 110, 111, 113, 114, 115, 116, 117, 202]
