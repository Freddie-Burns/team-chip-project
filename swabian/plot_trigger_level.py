import numpy as np
import matplotlib.pyplot as plt
from util import SETTINGS_DIR


sweep_data = np.load(SETTINGS_DIR / "SNSPD_trigger_level_sweep_121948.npz")
shaun_chs = sweep_data['shaun_chs']
print(sweep_data['shaun_chs'])
print(sweep_data['bias_current'])
trigger_levels = sweep_data['trigger_levels']
mean_counts = sweep_data['mean_count_rate']
std_counts = sweep_data['std_count_rate']
conf_nums = mean_counts.shape[1]
snr = mean_counts[1:].copy() / mean_counts[0]

fig1, axs1 = plt.subplots(2, 1, sharex=True, sharey=True)
fig2, axs2 = plt.subplots(2, 1, sharex=True)
for i, (ax1, ax2) in enumerate(zip(axs1, axs2)):
    for j in range(conf_nums):
        ax1.errorbar(trigger_levels, mean_counts[j, i, :].T, std_counts[j, i, :].T)
    for j in range(conf_nums - 1):
        ax2.plot(trigger_levels, snr[j, i, :])
    ax1.set_title(f'{i}: ch{shaun_chs[i]}')
    ax1.legend([f'conf{i}' for i in range(conf_nums)])
    ax1.set_xlabel('Trigger Level (V)')
    ax1.set_ylabel('Countrate (Hz)')
    # ax1.set_ylim(-1000, 11000)
    ax1.label_outer()
    ax2.set_title(f'{i}: ch{shaun_chs[i]}')
    ax2.legend([f'conf{i}' for i in range(conf_nums)])
    ax2.set_xlabel('Trigger Level (V)')
    ax2.set_ylabel('SNR')
    # ax2.set_ylim(-1000, 11000)
    ax2.label_outer()
plt.show()
