import matplotlib.pyplot as plt
import matplotlib


nice_fonts = {
        # use LaTeX to write all text
        # "text.usetex": True,
        "font.family": "sans-serif", # "sans-serif",
        # use 10pt font in plots, to match 10pt font in document
        "axes.labelsize": 14,
        "font.size": 14,
        # make the legend/label fonts a little smaller
        "legend.fontsize": 14,
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
}

matplotlib.rcParams.update(nice_fonts)

REMOVING_L1 = False

batch_sizes = [2, 4, 6, 8, 10]

jct_dynamic_sjfp = [1, 2, 3, 4, 5]
jct_static_sjfp = [2, 4, 6, 8, 10]
throughput_dynamic_sjfp = [4, 8, 12, 16, 20]
throughput_static_sjfp = [2, 4, 6, 8, 10]
jct_dynamic_baseline = [3, 6, 9, 12, 15]
jct_static_baseline = [6, 12, 18, 24, 30]
throughput_dynamic_baseline = [3, 6, 9, 12, 15]
throughput_static_baseline = [1, 2, 3, 4, 5]

fig_size_w = 10
fig_size_h = 3.5
num_cols = 4

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(fig_size_w, fig_size_h))

ax[0].plot(batch_sizes, jct_static_baseline, label='FCFS (dynamic)', marker='^', linestyle='--', color='#3065AC')
ax[0].plot(batch_sizes, jct_dynamic_baseline, label='FCFS (continuous)', marker='^', linestyle='-', color='#3065AC')
ax[0].plot(batch_sizes, jct_static_sjfp, label='SSJF (dynamic)', linestyle='--', marker='s', color='#A0BC71')
ax[0].plot(batch_sizes, jct_dynamic_sjfp, label='SSJF (continuous)', linestyle='-', marker='s', color='#A0BC71')
ax[0].set_ylim(bottom=0)

ax[1].plot(batch_sizes, throughput_static_baseline, label='FCFS (dynamic)', marker='^', linestyle='--', color='#3065AC')
ax[1].plot(batch_sizes, throughput_dynamic_baseline, label='FCFS (continuous)', marker='^', linestyle='-', color='#3065AC')
ax[1].plot(batch_sizes, throughput_static_sjfp, label='SSJF (dynamic)', linestyle='--', marker='s', color='#A0BC71')
ax[1].plot(batch_sizes, throughput_dynamic_sjfp, label='SSJF (continuous)', linestyle='-', marker='s', color='#A0BC71')
ax[1].set_ylim(bottom=0)

ax[0].set_xlabel('Batch Size')
ax[0].set_ylabel('JCT')
ax[1].set_xlabel('Batch Size')
ax[1].set_ylabel('Throughput')

ax[0].grid(True, axis='y', zorder=-1, linestyle='dashed', color='gray', alpha=0.5)
ax[1].grid(True, axis='y', zorder=-1, linestyle='dashed', color='gray', alpha=0.5)

# ax[1].legend(loc=(1.1, 0.5))
# put the shared legend at the bottom outside the figure
handles, labels = ax[0].get_legend_handles_labels()

# reducing the horizontal space between legend entries
fig.legend(handles, labels, loc='lower center', ncol=num_cols, bbox_to_anchor=(0.5, -0.02), columnspacing=0.5)

plt.tight_layout()
plt.show()