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

rounds = [0, 1, 2, 3, 4]
accuracy_per_round = [0.619, 0.600, 0.601, 0.610, 0.607, 0.615]
f1_weighted_per_round = [0.618, 0.599, 0.600, 0.601, 0.606, 0.615]
improvements_jct_per_round = [30, 31, 32, 31, 30, 33]

# plot
fig_size_w = 6
fig_size_h = 3

colors = ['#3065AC', '#2B7BBA', '#009DCC', '#15B1BA', '#A0BC71', '#FACE37', '#F2EA3B', 'indianred']
fig = plt.figure(figsize=(fig_size_w, fig_size_h))
ax = fig.add_subplot(111)
x = range(len(rounds) + 1)
ln1 = ax.plot(x, accuracy_per_round, label='Accuracy', color=colors[-1], linestyle='-', marker='o', markersize=10)
ln2 = ax.plot(x, f1_weighted_per_round, label='F1 Score', color=colors[0], linestyle='-', marker='^', markersize=10)

ax2 = ax.twinx()
ln3 = ax2.bar(x, improvements_jct_per_round, label='JCT', color=colors[4], width=0.5)

# lns = ln1 + ln2 + ln3  # + ln4
# labs = [l.get_label() for l in lns]
# ax.legend(lns, labs, loc=0, ncols=3, columnspacing=0.5)
ax.legend(loc='upper left', ncols=3, columnspacing=0.5)
ax2.legend(loc='upper right', ncols=1, columnspacing=0.5)

# ax.set_ylim(bottom=0.4, top=0.65)
ax.set_ylim(bottom=0.5, top=0.67)
# ax2.set_ylim(bottom=10, top=55)
ax2.set_ylim(bottom=10, top=57)

plt.xticks(x, ['R' + str(i+1) for i in rounds] + ['All'])
ax.set_xlabel('Round')
ax.set_ylabel('Predictor Performance')
ax2.set_ylabel('JCT Improvement (%)')
plt.grid(True, axis='y', zorder=-1, linestyle='dashed', color='gray', alpha=0.5)
plt.tight_layout()
plt.show()