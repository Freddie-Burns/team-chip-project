import numpy as np
import matplotlib.pyplot as plt
import time
from datetime import datetime
from TimeTaggerRPC import client
from swabian_param import swabian_host, swabian_port, swabian_ch1, swabian_ch2, swabian_chs, shaun_ch1, shaun_ch2, shaun_chs
import swabian.detectors as det
import util


def delatch():
    det.delatch(system='S', channel=shaun_ch1)
    det.delatch(system='S', channel=shaun_ch2)
    time.sleep(1)


def set_bias(current):
    for ch in shaun_chs:
        det.set_bias('S', ch, current)
    time.sleep(1)


conf_nums = 2
max_bias_current = 12
min_bias_current = 10
bias_currents_num = int((max_bias_current - min_bias_current) * 20 + 1)
print(f"Sweeping from {min_bias_current}mA to {max_bias_current}mA for {bias_currents_num} points")
duration = 10
bias_currents = np.linspace(min_bias_current, max_bias_current, bias_currents_num)
rates = np.empty((conf_nums, 2,) + bias_currents.shape, dtype='float64')
counts = np.empty((conf_nums, 2,) + bias_currents.shape + (duration,), dtype='float64')
with client.createProxy(host=swabian_host, port=swabian_port) as TT:
    tagger = TT.createTimeTagger()
    tagger.setTestSignal(swabian_ch1, False)
    tagger.setTestSignal(swabian_ch2, False)
    tagger.setDelayHardware(swabian_ch1, 0)
    tagger.setDelayHardware(swabian_ch2, 216)
    tagger.setDelaySoftware(swabian_ch1, 0)
    tagger.setDelaySoftware(swabian_ch2, 0)
    trigger_level = 0.075
    trigger_level1 = trigger_level
    trigger_level2 = trigger_level
    tagger.setTriggerLevel(swabian_ch1, trigger_level1)
    tagger.setTriggerLevel(swabian_ch2, trigger_level2)
    print(f'Setting trigger threshold to {trigger_level1}V and {trigger_level2}V')
    sync_measurements = TT.SynchronizedMeasurements(tagger)
    sync_tagger = sync_measurements.getTagger()
    rate_measure = TT.Countrate(sync_tagger, swabian_chs)
    counter_measure = TT.Counter(sync_tagger, swabian_chs, int(1e12), duration)
    tagger.sync()

    for i in range(conf_nums):
        for j, bias_current in enumerate(bias_currents):
            print(f"collecting#{j} bias={bias_current}mA")
            set_bias(bias_current)
            delatch()
            sync_measurements.startFor(int(1e12 * duration))
            while sync_measurements.isRunning():
                time.sleep(0.2)
            # This feature was added in v2.7.2, we are using v2.9.0,
            # so it should work, but it does not.
            # sync_measurements.waitUntilFinished()
            rate_data = rate_measure.getData()
            print(rate_data)
            rates[i, :, j] = rate_data
            count_data = counter_measure.getData()
            print(count_data)
            counts[i, :, j, :] = count_data
        # if i < conf_nums - 1:
        print("Please change configuration")
        input("Enter to continue.")
            # util.notify_mobile('Please change configuration')
            # if not user_confirm():
            #     break
        # else:
        #     util.notify_mobile('Characterisation done!')
    conf_nums = i + 1
    # Don't do this in Bristol, it will ruin other people's measurement
    # TT.freeTimeTagger(tagger)

print(rates)
print(counts)

mean_counts = np.mean(counts, axis=-1)
std_counts = np.std(counts, axis=-1, ddof=1)
snr = mean_counts[1:].copy() / mean_counts[0]

measurement_time = datetime.now()
save_dir = util.get_save_dir()
np.savez(
    save_dir / 'SNSPD_bias_current_sweep_{:%H%M%S}.npz'.format(measurement_time),
    shaun_chs=np.array(shaun_chs),
    trigger_level=np.array([trigger_level1, trigger_level2]),
    bias_currents=bias_currents,
    mean_count_rate=mean_counts,
    std_count_rate=std_counts,
)

fig1, axs1 = plt.subplots(2, 1, sharex=True)
fig2, axs2 = plt.subplots(2, 1, sharex=True)
for i, (ax1, ax2) in enumerate(zip(axs1, axs2)):
    for j in range(conf_nums):
        ax1.errorbar(bias_currents, mean_counts[j, i, :].T, std_counts[j, i, :].T)
    for j in range(conf_nums - 1):
        ax2.plot(bias_currents, snr[j, i, :])
    ax1.set_title(f'{i}: ch{swabian_chs[i]}')
    ax1.legend([f'conf{i}' for i in range(conf_nums)])
    ax1.set_xlabel('Bias Currents (mA)')
    ax2.set_title(f'{i}: ch{swabian_chs[i]}')
    ax2.legend([f'conf{i}' for i in range(conf_nums)])
    ax2.set_xlabel('Bias Currents (mA)')
    ax1.set_ylabel('Countrate (Hz)')
    ax2.set_ylabel('SNR')
    ax1.label_outer()
    ax2.label_outer()
plt.show()
