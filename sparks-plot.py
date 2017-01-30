import pandas as pd
from matplotlib import pylab as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits.mplot3d import axes3d, Axes3D  # <-- Note the capitalization!

dataset = "netbeans"
# dataset = "eclipse"
# dataset = "firefox"

# Particle Swarm
ps_df = pd.read_csv('data/' + dataset + '/ps_out.csv')

# Nelder-Mead
nm_df = pd.read_csv('data/' + dataset + '/nm_out.csv')

# Random search
rnd_df = pd.read_csv('data/' + dataset + '/rnd_out.csv')

# Grid search
g_df = pd.read_csv('data/' + dataset + '/g_out.csv')

# cutoff = 0.5

fig = plt.figure(facecolor='white')
# ax = Axes3D(ax1)

plt.subplots_adjust(wspace=.05, hspace=.05)

ax = fig.add_subplot(2, 2, 1, projection='3d')
ax.set_title("Particle Swarm")

ax.scatter(xs=ps_df['categoryScalingFactor'],
           ys=ps_df['productScalingFactor'],
           zs=ps_df['value'])

ax.set_xlabel('Component_Id Multiplier')
ax.set_ylabel('Product_Id Multiplier')
ax.set_zlabel('F-measure')

ax = fig.add_subplot(2, 2, 2, projection='3d')
ax.set_title("Nelder-Mead")

ax.scatter(xs=nm_df['categoryScalingFactor'],
           ys=nm_df['productScalingFactor'],
           zs=nm_df['value'])

ax.set_xlabel('Component_Id Multiplier')
ax.set_ylabel('Product_Id Multiplier')
ax.set_zlabel('F-measure')

ax = fig.add_subplot(2, 2, 3, projection='3d')
ax.set_title("Random Search")

ax.scatter(xs=rnd_df['categoryScalingFactor'],
           ys=rnd_df['productScalingFactor'],
           zs=rnd_df['value'])

ax.set_xlabel('Component_Id Multiplier')
ax.set_ylabel('Product_Id Multiplier')
ax.set_zlabel('F-measure')

ax = fig.add_subplot(2, 2, 4, projection='3d')
ax.set_title("Grid Search")

ax.scatter(xs=g_df['categoryScalingFactor'],
           ys=g_df['productScalingFactor'],
           zs=g_df['value'])

ax.set_xlabel('Component_Id Multiplier')
ax.set_ylabel('Product_Id Multiplier')
ax.set_zlabel('F-measure')

plt.show()
