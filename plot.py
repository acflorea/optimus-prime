import matplotlib.pyplot as plt
import numpy as np

N = 300
multiplier = 1

# n
x = np.arange(1, N + 1)
# targeted stop
y = np.arange(1, multiplier * N + 1)

# lines, columns
p = np.zeros((N + 1, multiplier * N + 1))

for n in x:
    for m in y:
        p[n, m] = 100 * float(n) / (multiplier * N) * max(0.0, min(1, np.log(m) - np.log(n)))

fig, ax = plt.subplots(figsize=(6, 6))
# 1st axis is X, 2nd is Y
ax.imshow(p
          , cmap='ocean'
          , interpolation='none'
          , origin='lower'
          , aspect="auto"
          # , extent=[1, multiplier * N + 1, 1, N + 1]
          )

plt.show()
