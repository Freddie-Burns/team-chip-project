from pathlib import Path
from TimeTaggerRPC import client
from parameters import swabian_host, swabian_port, swabian_ch1, swabian_ch2
import json
import matplotlib.pyplot as plt
import numpy as np

from util import timestamp

device = "testing"
binwidth = 5
n_bins = 50
trigger = 0.07
duration = 60
testing = True

fig, ax = plt.subplots()
plt.show(block=False)


with client.createProxy(host=swabian_host, port=swabian_port) as TT:
    tagger = TT.createTimeTagger()
    tagger.setTestSignal(swabian_ch1, testing)
    tagger.setTestSignal(swabian_ch2, testing)
    tagger.setDelayHardware(swabian_ch1, 0)
    tagger.setDelayHardware(swabian_ch2, 200)
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

    hist = TT.Correlation(tagger, swabian_ch1, swabian_ch2, binwidth=binwidth, n_bins=n_bins)
    # print(dir(hist))
    hist.startFor(int(duration*1e12), clear=True)

    x = hist.getIndex()
    while hist.isRunning():
        plt.pause(0.1)
        y = hist.getData()
        ax.clear()
        ax.plot(x, y)
        # ax.set_xlim(-325, -225)

    filename = f"{device} binwidth_{binwidth}ps trigger_{trigger}V {timestamp()}.csv"
    save_path = Path("../data/swabian")
    file_path = save_path / filename
    data = np.stack((x, y), axis=1)
    np.savetxt(file_path, data, delimiter=',')

    print("Done!")
    plt.show()
