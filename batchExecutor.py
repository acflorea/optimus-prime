import sys
from subprocess import call


def main(args):
    # /Users/aflorea/phd/optimus-prime/optunity_libsvm.py
    executor = args[1]

    # /Users/aflorea/phd/optimus-prime/crossVal.py
    script = args[2]

    # /Users/aflorea/phd/libsvm-datasets
    datasetsRootFolder = args[3]

    datasets = ['/cancer/breast-cancer_scale.libsvm',
                '/diabetes/diabetes_scale.libsvm',
                '/iris/iris.libsvm',
                '/poker/poker.libsvm',
                '/wine/wine.libsvm',
                '/adult/a1a.libsvm',
                '/adult/a6a.libsvm',
                ]

    solvers = {'particle swarm': 'ps',
               'nelder-mead': 'nm',
               'random search': 'rnd',
               'grid search': 'g',
               }

    algorithms = {"ManagerWorker": "MW",
                  "Leapfrog": "LF",
                  "SeqSplit": "SS",
                  "Parametrization": "P",
                  }

    targetStops = [50, 100, 150, 200, 250, 0]

    optunity = False
    go = True

    for dataset in datasets:

        if go:
            for algorithm in algorithms:
                for targetStop in targetStops:
                    # Build the output file name
                    outputFileName = datasetsRootFolder + dataset + \
                                     "." + algorithms[algorithm] + \
                                     "." + targetStop + '.log'

                    call(["/Users/aflorea/goworkspace/bin/goptim",
                          "-fileName", datasetsRootFolder + dataset,
                          "-maxAttempts", "250",
                          "-fct", "Script",
                          "-noOfExperiments", "10",
                          "-alg", algorithm,
                          "-script", script,
                          "-targetstop", targetStop
                          ],
                         stdout=open(outputFileName, 'w'),
                         stderr=open(outputFileName, 'w'),
                         cwd=datasetsRootFolder)

        if optunity:
            for solver in solvers:
                # Build the output file name
                outputFileName = datasetsRootFolder + dataset + "." + solvers[solver] + '.log'

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
                      solver
                      ],
                     stdout=open(outputFileName, 'w'),
                     stderr=open(outputFileName, 'w'),
                     cwd=datasetsRootFolder)


if __name__ == "__main__":
    # execute only if run as a script
    main(sys.argv)
