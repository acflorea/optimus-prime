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
models.append(('ManagerWorker', np.array([164, 169, 172, 223, 224, 194])))
models.append(('SequenceSplit', np.array([194, 133, 167, 203, 156, 215])))
models.append(('LeapFrog', np.array([194, 203, 214, 220, 189, 162])))
models.append(('Parametrization', np.array([148, 138, 187, 130, 158, 177])))
# models.append(('Optunity - RS', np.array([250])))
# models.append(('Optunity - GS', np.array([240])))
# models.append(('Optunity - PS', np.array([250])))
# models.append(('Optunity - NM', np.array([108, 142, 17, 6, 6, 62])))
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
fig.suptitle('Number of runs per type of parallel random generator')
ax = fig.add_subplot(111)
plt.boxplot(results)
ax.set_xticklabels(names)

plt.savefig("pp.pdf", format='pdf')
# plt.show()
