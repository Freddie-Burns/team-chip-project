from pathlib import Path
from TimeTaggerRPC import client
from parameters import swabian_host, swabian_port, swabian_ch1, swabian_ch2
import json
from time import sleep
import matplotlib.pyplot as plt
import numpy as np

from util import timestamp

# binwidth = 1000
# n_bins = 100
# trigger = 0.09
# power = 8  # dBm
# duration = 60

binwidth = 1000
n_bins = 100
trigger = 0.02
power = 8  # dBm
duration = 5

channel_a = swabian_ch2
channel_b = swabian_ch1

device = "ring-12"
testing = False

# fig, ax = plt.subplots()
# plt.show(block=False)


with client.createProxy(host=swabian_host, port=swabian_port) as TT:
    tagger = TT.createTimeTagger()
    tagger.setTestSignal(swabian_ch1, testing)
    tagger.setTestSignal(swabian_ch2, testing)
    tagger.setDelayHardware(swabian_ch1, 0)
    tagger.setDelayHardware(swabian_ch2, 0)
    tagger.setDelaySoftware(swabian_ch1, 0)
    tagger.setDelaySoftware(swabian_ch2, 0)
    tagger.setTriggerLevel(swabian_ch1, trigger)
    tagger.setTriggerLevel(swabian_ch2, trigger)
    tagger.sync()
    conf = tagger.getConfiguration()
    print("Swabian connected")
    print("tagger uri: ", tagger._pyroUri)
    # print(dir(tagger))
    with open("swabian_conf.json", 'w') as conf_file:
        json.dump(conf, conf_file, indent=4)


    time_tagger = TT.createTimeTagger()
    sync = TT.SynchronizedMeasurements(time_tagger)
    singles_counter = TT.Counter(tagger, [channel_a, channel_b], binwidth=int(duration * 1e12), n_values=1)
    singles_counter.startFor(int(duration * 1e12), clear=True)
    sleep(duration+1)
    sync.registerMeasurement(singles_counter)
    print(singles_counter.getData())
