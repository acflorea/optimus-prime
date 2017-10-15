import math
import numpy as np
import matplotlib.pyplot as plt

N = 300

x = np.arange(1.0, N, 1.0)

m = 200.0

# Pstar = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2]
Pstar = [1.0, 0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6]

# Pstar = [0.735]

P = np.zeros((len(Pstar), N - 1))

index = 0
for prob in Pstar:
    P[index] = x / 300 * np.log(prob * math.e * 300 / x) / prob
    index = index + 1

for p in P:
    plt.plot(x/300, p, label = p)

plt.plot(x/300, x/300, label = p)
plt.grid(True)
plt.show()
