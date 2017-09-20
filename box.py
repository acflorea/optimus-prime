# Compare Algorithms
import pandas
import matplotlib.pyplot as plt
import numpy as np

# load dataset
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/pima-indians-diabetes/pima-indians-diabetes.data"
names = ['preg', 'plas', 'pres', 'skin', 'test', 'mass', 'pedi', 'age', 'class']
dataframe = pandas.read_csv(url, names=names)
array = dataframe.values
X = array[:, 0:8]
Y = array[:, 8]
# prepare configuration for cross validation test harness
seed = 7
# prepare models
models = []
models.append(('GO-MW', np.array([164, 169, 172, 223, 224, 194])))
models.append(('GO-SS', np.array([194, 133, 167, 203, 156, 215])))
models.append(('GO-LF', np.array([194, 203, 214, 220, 189, 162])))
models.append(('GO-P', np.array([148, 138, 187, 130, 158, 177])))
models.append(('Opt-RS', np.array([250])))
models.append(('Opt-GS', np.array([240])))
models.append(('Opt-PS', np.array([250])))
models.append(('Opt-NM', np.array([108, 142, 17, 6, 6, 62])))
# evaluate each model in turn
results = []

names = []
scoring = 'accuracy'
for name, cv_results in models:
    results.append(cv_results)
    names.append(name)
    msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
    print(msg)
# boxplot algorithm comparison
fig = plt.figure()
fig.suptitle('Algorithm Comparison')
ax = fig.add_subplot(111)
plt.boxplot(results)
ax.set_xticklabels(names)
plt.show()
