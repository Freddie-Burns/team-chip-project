import numpy as np
import matplotlib.pyplot as plt
import time
from datetime import datetime
from util import user_confirm
from TimeTaggerRPC import client
from swabian_param import \
    swabian_host, swabian_port, swabian_ch1, swabian_ch2, swabian_chs, shaun_ch1, shaun_ch2, shaun_chs
import cryo_labs.detectors as det
import util


def delatch():
    det.delatch(system='S', channel=shaun_ch1)
    det.delatch(system='S', channel=shaun_ch2)
    time.sleep(1)


def set_bias(current1, current2=None):
    if current2 is None:
        current2 = current1
    for ch, current in zip(shaun_chs, (current1, current2)):
        det.set_bias('S', ch, current)
    time.sleep(1)


conf_nums = 2
# dark count roll off at around 0.02 V
# max_trigger_level = 0.025
max_trigger_level = 0.175
trigger_levels_num = 32
trigger_levels = np.linspace(0.02, max_trigger_level, trigger_levels_num)[1:]
print(f'Sweeping from 0V to {max_trigger_level}V for {trigger_levels_num-1}')
rates = np.empty((conf_nums, 2,) + trigger_levels.shape, dtype='float64')
counts = np.empty((conf_nums, 2,) + trigger_levels.shape + (10,), dtype='float64')
with client.createProxy(host=swabian_host, port=swabian_port) as TT:
    tagger = TT.createTimeTagger()
    tagger.setTestSignal(swabian_ch1, False)
    tagger.setTestSignal(swabian_ch2, False)
    tagger.setDelayHardware(swabian_ch1, 0)
    tagger.setDelayHardware(swabian_ch2, 216)
    tagger.setDelaySoftware(swabian_ch1, 0)
    tagger.setDelaySoftware(swabian_ch2, 0)
    sync_measurements = TT.SynchronizedMeasurements(tagger)
    sync_tagger = sync_measurements.getTagger()
    rate_measure = TT.Countrate(sync_tagger, swabian_chs)
    counter_measure = TT.Counter(sync_tagger, swabian_chs, int(1e12), 10)
    bias_currents = (10, 11)
    print(f'Setting bias to {bias_currents} mA')
    set_bias(*bias_currents)

    for i in range(conf_nums):
        for j, trigger_level in enumerate(trigger_levels):
            print(f"collecting#{j} trigger={trigger_level}V")
            tagger.setTriggerLevel(swabian_ch1, trigger_level)
            tagger.setTriggerLevel(swabian_ch2, trigger_level)
            delatch()
            tagger.sync()
            sync_measurements.startFor(int(10e12))
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
        if i < conf_nums - 1:
            print("Please change configuration")
            util.notify_mobile('Please change configuration')
            if not user_confirm():
                break
        else:
            util.notify_mobile('Characterisation done!')
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
    save_dir / 'SNSPD_trigger_level_sweep_{:%H%M%S}.npz'.format(measurement_time),
    shaun_chs=np.array(shaun_chs),
    bias_current=np.array(bias_currents),
    trigger_levels=trigger_levels,
    mean_count_rate=mean_counts,
    std_count_rate=std_counts,
)

fig1, axs1 = plt.subplots(2, 1, sharex=True, sharey=True)
fig2, axs2 = plt.subplots(2, 1, sharex=True)
for i, (ax1, ax2) in enumerate(zip(axs1, axs2)):
    for j in range(conf_nums):
        ax1.errorbar(trigger_levels, mean_counts[j, i, :].T, std_counts[j, i, :].T)
    for j in range(conf_nums - 1):
        ax2.plot(trigger_levels, snr[j, i, :])
    ax1.set_title(f'{i}: ch{swabian_chs[i]}')
    ax1.legend([f'conf{i}' for i in range(conf_nums)])
    ax1.set_xlabel('Trigger Level (V)')
    ax1.set_ylabel('Countrate (Hz)')
    # ax1.set_ylim(-1000, 11000)
    ax1.label_outer()
    ax2.set_title(f'{i}: ch{swabian_chs[i]}')
    ax2.legend([f'conf{i}' for i in range(conf_nums)])
    ax2.set_xlabel('Trigger Level (V)')
    ax2.set_ylabel('SNR')
    # ax2.set_ylim(-1000, 11000)
    ax2.label_outer()
plt.show()
