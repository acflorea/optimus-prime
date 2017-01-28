import pandas as pd
from matplotlib import pylab as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits.mplot3d import axes3d, Axes3D  # <-- Note the capitalization!

# dataset = "netbeans"
# baseline = 0.5
# dataset = "eclipse"
# baseline = 0.5
dataset = "firefox"
baseline = 0.5

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

base, = plt.plot([baseline] * 300, '--', label='Baseline')
ps, = plt.plot(ps, 'r1', ms=15, label='Particle Swarm')
nm, = plt.plot(nm, 'g2', ms=15, label='Nelder-Mead')
rnd, = plt.plot(rnd, 'b3', ms=15, label='Random Search')
g, = plt.plot(g, 'c4', ms=15, label='Grid Search')

plt.legend(loc=4, handles=[base, ps, nm, rnd, g])

plt.show()
