from sklearn.datasets import load_svmlight_file
from sklearn.model_selection import cross_val_score
from sklearn import svm
import sys
import time


def main(args):
    # "/Users/aflorea/phd/libsvm-datasets/adult/a1a.libsvm" "rbf" 1 "auto" 3 0.0
    fileName = args[1]
    kernel = args[2]
    C = float(args[3])
    Gamma = args[4]
    if Gamma != 'auto':
        Gamma = float(Gamma)
    Degree = int(args[5])
    Coef0 = float(args[6])

    dataset = load_svmlight_file(fileName)

    start_time = time.time()

    X_train = dataset[0].todense()
    y_train = dataset[1]

    clf = svm.SVC(kernel=kernel, C=C, degree=Degree, coef0=Coef0, gamma=Gamma)  # .fit(X_train, y_train)

    # print(kernel, C, Degree, Coef0, Gamma)

    scores = cross_val_score(clf, X_train, y_train, cv=10)

    # print("--- %s seconds ---" % (time.time() - start_time))

    # calculate stuff
    # sys.stdout.write(','.join(args))
    sys.stdout.write(','.join(str(e) for e in scores))
    sys.stdout.flush()
    sys.exit(0)


if __name__ == "__main__":
    # execute only if run as a script
    main(sys.argv)
