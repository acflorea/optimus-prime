import optunity
import optunity.metrics

import sklearn.svm

from sklearn.datasets import load_digits, load_svmlight_file

import time

dataset = load_svmlight_file("/Users/acflorea/phd/libsvm-datasets/adult/a1a.libsvm")

n = dataset[1].size

positive_label = 1.0
negative_lable = -1.0

positive_idx = [i for i in range(n) if dataset[1][i] == positive_label]
negative_idx = [i for i in range(n) if dataset[1][i] == negative_lable]

# add some noise to the data to make it a little challenging
labels = [True] * len(positive_idx) + [False] * len(negative_idx)

# we will make the cross-validation decorator once, so we can reuse it later for the other tuning task
# by reusing the decorator, we get the same folds etc.
cv_decorator = optunity.cross_validated(x=dataset[0].todense(), y=dataset[1], num_folds=10)


def svm_rbf_tuned_acc(x_train, y_train, x_test, y_test, C, logGamma):
    model = sklearn.svm.SVC(C=C, gamma=10 ** logGamma).fit(x_train, y_train)
    y_hat = model.predict(x_test)
    acc = optunity.metrics.accuracy(y_test, y_hat)
    print (C, logGamma, acc)
    return acc


svm_rbf_tuned_acc = cv_decorator(svm_rbf_tuned_acc)
# this is equivalent to the more common syntax below
# @optunity.cross_validated(x=data, y=labels, num_folds=5)
# def svm_rbf_tuned_auroc...

start_time = time.time()

optimal_rbf_pars, info, _ = optunity.maximize(svm_rbf_tuned_acc, num_evals=150, C=[0, 10], logGamma=[-5, 0],
                                              pmap=optunity.pmap)

print("Optimal parameters: " + str(optimal_rbf_pars))
print("ACC of tuned SVM with RBF kernel: %1.3f" % info.optimum)

print("--- %s seconds ---" % (time.time() - start_time))
