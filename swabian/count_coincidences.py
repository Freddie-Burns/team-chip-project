from pathlib import Path
from TimeTaggerRPC import client
import json
import matplotlib.pyplot as plt
import numpy as np

from parameters import swabian_host, swabian_port, swabian_ch1, swabian_ch2
from util import timestamp

# Default values
# binwidth = 1000
# n_bins = 100
# trigger = 0.09
# power = 8  # dBm
# duration = 60

# Run parameters
BINWIDTH = 1000
DATA_DIR = Path("../data/swabian")
DEVICE = "test"
DURATION = 5
N_BINS = 200
POWER = 5  # dBm
SAVE = False
TESTING = False
TRIGGER = 0.05


with client.createProxy(host=swabian_host, port=swabian_port) as TT:
    tagger = TT.createTimeTagger()
    tagger.setTestSignal(swabian_ch1, TESTING)
    tagger.setTestSignal(swabian_ch2, TESTING)
    tagger.setDelayHardware(swabian_ch1, 0)  # 51700
    tagger.setDelayHardware(swabian_ch2, 0)
    tagger.setDelaySoftware(swabian_ch1, 0)
    tagger.setDelaySoftware(swabian_ch2, 0)
    tagger.setTriggerLevel(swabian_ch1, TRIGGER)
    tagger.setTriggerLevel(swabian_ch2, TRIGGER)
    tagger.sync()
    conf = tagger.getConfiguration()
    print("Swabian connected")
    print("tagger uri: ", tagger._pyroUri)
    with open("swabian_conf.json", 'w') as conf_file:
        json.dump(conf, conf_file, indent=4)

    # coin_groups = [[1, 2]]
    # coin_vc = TT.Coincidences(tagger, coincidenceGroups=coin_groups, coincidenceWindow=binwidth)
    # coin_channels = coin_vc.getChannels()

    singles_counter = TT.Counter(
        tagger,
        channels=(swabian_ch1, swabian_ch2),
        binwidth=int(DURATION * 1e12),
        n_values=1,
    )

    hist = TT.Correlation(
        tagger,
        swabian_ch1,
        swabian_ch2,
        binwidth=BINWIDTH,
        n_bins=N_BINS,
    )

    singles_counter.startFor(int(DURATION * 1e12), clear=True)
    hist.startFor(int(DURATION * 1e12), clear=True)

    # Live plot coincidences
    fig, ax = plt.subplots()
    plt.show(block=False)
    x = hist.getIndex()

    while hist.isRunning():
        plt.pause(0.1)
        y = hist.getData()
        ax.clear()
        ax.plot(x, y)

    # Measure single counts for each channel
    singles = singles_counter.getData()

    # Save total coincidence histogram
    filename = f"{DEVICE} binwidth_{BINWIDTH}ps trigger_{TRIGGER}V power_{POWER}dBm integration_{DURATION}s {timestamp()}.csv"
    file_path = DATA_DIR / "coincidences" / filename
    data = np.stack((x, y), axis=1)
    if SAVE: np.savetxt(file_path, data, delimiter=',')

    # Save single counts
    print(f"Singles: {singles}")
    file_path = DATA_DIR / "single_counts" / filename
    data = np.stack(singles, axis=1)
    if SAVE: np.savetxt(file_path, data, delimiter=',')

    print("Done!")
    plt.show()
