import sys
from subprocess import call


def main(args):
    # /Users/aflorea/phd/optimus-prime/optunity_libsvm.py
    executor = args[1]

    # /Users/aflorea/phd/optimus-prime/crossVal.py
    script = args[2]

    # /Users/aflorea/phd/libsvm-datasets
    datasetsRootFolder = args[3]

    datasets = ['/adult/a1a.libsvm',
                '/cancer/breast-cancer_scale.libsvm',
                '/diabetes/diabetes_scale.libsvm',
                '/iris/iris.libsvm',
                '/poker/poker.libsvm',
                '/wine/wine.libsvm'
                ]

    for dataset in datasets:
        # Build the output file name
        outputFileName = datasetsRootFolder + dataset + '.log'

        # python
        # optunity_libsvm.py
        # "/Users/aflorea/phd/optimus-prime/crossVal.py" "/Users/aflorea/phd/libsvm-datasets/adult/a1a.libsvm"
        # 250
        # "random search"

        call(["python",
              executor,
              script,
              datasetsRootFolder + dataset,
              "250",
              "random search"
              ],
             stdout=open(outputFileName, 'w'),
             stderr=open(outputFileName, 'w'),
             cwd=datasetsRootFolder)


if __name__ == "__main__":
    # execute only if run as a script
    main(sys.argv)
