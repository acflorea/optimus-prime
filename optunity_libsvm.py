import optunity
import optunity.metrics

import sklearn.svm
import numpy as np

from sklearn.datasets import load_digits

digits = load_digits()
n = digits.data.shape[0]

positive_digit = 8
negative_digit = 9

positive_idx = [i for i in range(n) if digits.target[i] == positive_digit]
negative_idx = [i for i in range(n) if digits.target[i] == negative_digit]

# add some noise to the data to make it a little challenging
original_data = digits.data[positive_idx + negative_idx, ...]
data = original_data + 5 * np.random.randn(original_data.shape[0], original_data.shape[1])
labels = [True] * len(positive_idx) + [False] * len(negative_idx)


# we will make the cross-validation decorator once, so we can reuse it later for the other tuning task
# by reusing the decorator, we get the same folds etc.
cv_decorator = optunity.cross_validated(x=data, y=labels, num_folds=10)

def svm_rbf_tuned_acc(x_train, y_train, x_test, y_test, C, logGamma):
    model = sklearn.svm.SVC(C=C, gamma=10 ** logGamma).fit(x_train, y_train)
    y_hat = model.predict(x_test)
    acc = optunity.metrics.accuracy(y_test, y_hat)
    return acc


svm_rbf_tuned_acc = cv_decorator(svm_rbf_tuned_acc)
# this is equivalent to the more common syntax below
# @optunity.cross_validated(x=data, y=labels, num_folds=5)
# def svm_rbf_tuned_auroc...

print svm_rbf_tuned_acc(C=4.633138020833334, logGamma=-2.8818894810828026)

optimal_rbf_pars, info, _ = optunity.maximize(svm_rbf_tuned_acc, num_evals=150, C=[0, 10], logGamma=[-5, 0],
                                              pmap=optunity.pmap)

print("Optimal parameters: " + str(optimal_rbf_pars))
print("ACC of tuned SVM with RBF kernel: %1.3f" % info.optimum)
