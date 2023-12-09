import requests


url = 'http://det.phy.bris.ac.uk'
REGEX = '\"(.*)\\n\"'
MAXVOLTAGE = 2.25  # Volts
MAXCURRENT = 25  # micro Amps


def set_bias(system, channel, current_uA):
    # Set bias current NEW PHOTONSPOT SYSTEMS
    # Channel is either int (1-24) or channel string i.e. CTRL2_A1
    if not -MAXCURRENT <= current_uA <= MAXCURRENT:
        print('Please set the voltage to an interval between -%s uA to +%s uA' % (MAXCURRENT, MAXCURRENT))
        return
    command = '/bias2.php?cmd=bias_set&system={:}&channel={:}&current={:}'.format(system, channel, current_uA)
    requests.post(url + command)


def delatch(system, channel):
    # Delatch the channel
    command = '/bias2.php?cmd=delatch&system={:}&channel={:}'.format(system, channel)
    requests.post(url + command)
