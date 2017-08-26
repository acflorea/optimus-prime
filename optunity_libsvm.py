import optunity
import optunity.metrics
from subprocess import Popen, PIPE
import time
import sys

scriptName = ""
fileName = ""


def main(args):
    start_time = time.time()

    global scriptName
    scriptName = args[1]
    global fileName
    fileName = args[2]

    search = {
        'kernel': {'linear': {'C': [0, 10]},
                   'rbf': {'gamma': [0, 1], 'C': [0, 10]},
                   'poly': {'degree': [2, 5], 'C': [0, 10], 'coef0': [0, 1]}
                   }
    }

    optimal_rbf_pars, info, _ = optunity.maximize_structured(external_svm, num_evals=150, search_space=search,
                                                             pmap=optunity.pmap)

    print("Optimal parameters: " + str(optimal_rbf_pars))
    print("Optimal value: " + str(info.optimum))

    print("--- %s seconds ---" % (time.time() - start_time))


def external_svm(kernel, C, gamma, degree, coef0):
    if gamma == None:
        gamma = "auto"

    if degree == None:
        degree = "3"
    else:
        degree = int(round(degree))

    if coef0 == None:
        coef0 = "0.0"

    process = Popen(["python", scriptName, fileName, kernel, str(C), str(gamma), str(degree), str(coef0)], stdout=PIPE)

    (output, err) = process.communicate()

    values = map(float, str(output).split(","))

    print values

    return sum(values) / len(values)


if __name__ == "__main__":
    # execute only if run as a script
    main(sys.argv)
