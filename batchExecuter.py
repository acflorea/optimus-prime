import sys


def main(args):

    # /Users/aflorea/phd/libsvm-datasets
    datasetsRootFolder = args[1]

    datasets = ['/adult/a6a.libsvm',
                'cancer/breast-cancer_scale.libsvm',
                '/diabetes/diabetes_scale.libsvm',
                '/iris/iris.libsvm',
                '/poker/poker.libsvm',
                'wine/wine.libsvm'
                ]


if __name__ == "__main__":
    # execute only if run as a script
    main(sys.argv)
