import optunity
import optunity.metrics
from optunity import search_spaces, api
from optunity import functions as fun
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

    search_space = {
        'kernel': {'linear': {'C': [0, 10]},
                   'rbf': {'gamma': [0, 1], 'C': [0, 10]},
                   'poly': {'degree': [2, 5], 'C': [0, 10], 'coef0': [0, 1]}
                   }
    }

    f = external_svm
    num_evals = 150

    tree = search_spaces.SearchTree(search_space)
    box = tree.to_box()

    # we need to position the call log here
    # because the function signature used later on is internal logic
    f = fun.logged(f)

    # wrap the decoder and constraints for the internal search space representation
    f = tree.wrap_decoder(f)
    f = api._wrap_hard_box_constraints(f, box, -sys.float_info.max)

    suggestion = api.suggest_solver(num_evals, "particle swarm", **box)
    solver = api.make_solver(**suggestion)
    solution, details = api.optimize(solver, f, maximize=True, max_evals=num_evals,
                                     pmap=optunity.pmap, decoder=tree.decode)

    print("Optimal parameters: " + str(solution))
    print("Optimal value: " + str(details.optimum))

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
    average = sum(values) / len(values)

    print values, average

    return average


if __name__ == "__main__":
    # execute only if run as a script
    main(sys.argv)
