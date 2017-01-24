import pandas as pd
from matplotlib import pylab as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D  # <-- Note the capitalization!

# dataset = "netbeans"
# dataset = "eclipse"
dataset = "firefox"

# Particle Swarm
df = pd.read_csv('data/' + dataset + '/ps_out.csv')

# Nelder-Mead
# df = pd.read_csv('data/' + dataset + '/nm_out.csv')

# Random search
# df = pd.read_csv('data/' + dataset + '/rnd_out.csv')

# Grid search
# df = pd.read_csv('data/' + dataset + '/g_out.csv')

cutoff = 0.5
fig = plt.figure()
ax = Axes3D(fig)

ax.scatter(xs=df['categoryScalingFactor'],
           ys=df['productScalingFactor'],
           zs=df['value'])

# ax.scatter(xs=df[df.value > cutoff]['categoryScalingFactor'],
#            ys=df[df.value > cutoff]['productScalingFactor'],
#            zs=df[df.value > cutoff]['value'])

ax.set_xlabel('categoryScalingFactor')
ax.set_ylabel('productScalingFactor')
ax.set_zlabel('F1')

plt.show()
