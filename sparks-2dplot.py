import pandas as pd
from matplotlib import pylab as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits.mplot3d import axes3d, Axes3D  # <-- Note the capitalization!

dataset = "netbeans"
baseline00 = 0.71
baseline11 = 0.71
# Weighted Precision = 0.807814580153602
# Weighted Recall = 0.7667638483965015
# Weighted fMeasure = 0.7691632413077985
# dataset = "eclipse"
# baseline = 0.64
# Weighted Precision = 0.6432892308806841
# Weighted Recall = 0.5969945355191255
# Weighted fMeasure = 0.5943210252864047
# dataset = "firefox"
# baseline = 0.68
# Weighted Precision = 0.7125398556722572
# Weighted Recall = 0.6978798586572442
# Weighted fMeasure = 0.680808398657662

# Particle Swarm
ps_df = pd.read_csv('data/' + dataset + '/ps_out.csv')

# Nelder-Mead
nm_df = pd.read_csv('data/' + dataset + '/nm_out.csv')

# Random search
rnd_df = pd.read_csv('data/' + dataset + '/rnd_out.csv')

# Grid search
g_df = pd.read_csv('data/' + dataset + '/g_out.csv')

fig = plt.figure(facecolor='white')
# ax = Axes3D(ax1)

ps = ps_df['value']
nm = nm_df['value']
rnd = rnd_df['value']
g = g_df['value']

base0, = plt.plot([baseline00] * 300, 'k-.', label='Baseline 0')
base1, = plt.plot([baseline11] * 300, 'k--', label='Baseline 1')
ps, = plt.plot(ps, 'g', ms=15, label='Particle Swarm', linewidth=1.0)
rnd, = plt.plot(rnd, 'b', ms=15, label='Random Search', linewidth=1.0)
g, = plt.plot(g, 'c', ms=15, label='Grid Search',    linewidth=1.0)
nm, = plt.plot(nm, 'r', ms=15, label='Nelder-Mead', linewidth=1.0)

plt.legend(loc=3, handles=[base0, base1, ps, nm, rnd, g])

plt.xlabel('Run number')
plt.ylabel('F-measure')

plt.show()
