from pathlib import Path
from TimeTaggerRPC import client
from parameters import swabian_host, swabian_port, swabian_ch1, swabian_ch2
import json
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
trigger = 0.03
power = 8  # dBm
duration = 60

device = "ring-16"
testing = False

fig, ax = plt.subplots()
plt.show(block=False)


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

    hist = TT.Counter(tagger, [swabian_ch2], binwidth=binwidth, n_values=n_bins)
    # print(dir(hist))
    hist.startFor(int(duration*1e12), clear=True)

    x = hist.getIndex()
    while hist.isRunning():
        plt.pause(0.1)
        y = hist.getData()[0]
        ax.clear()
        ax.plot(x, y)
        # ax.set_xlim(-325, -225)

    filename = f"{device} binwidth_{binwidth}ps trigger_{trigger}V power_{power}dBm {timestamp()}.csv"
    save_path = Path("../data/swabian")
    file_path = save_path / filename
    data = np.stack((x, y), axis=1)
    np.savetxt(file_path, data, delimiter=',')

    print("Done!")
    plt.show()
