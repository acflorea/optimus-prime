from sklearn.datasets import load_svmlight_file
from sklearn.cross_validation import cross_val_score
from sklearn import svm
import sys

def main(args):
    dataset = load_svmlight_file("/Users/acflorea/phd/libsvm-datasets/adult/a1a.libsvm")

    X_train = dataset[0].todense()
    y_train = dataset[1]

    clf = svm.SVC(kernel='linear', C=1).fit(X_train, y_train)

    scores = cross_val_score(clf, X_train, y_train, cv=10)

    sys.exit(scores)

if __name__ == "__main__":
    # execute only if run as a script
    main(sys.argv)