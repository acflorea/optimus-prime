from subprocess import call
import optunity

from matplotlib import pylab as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D  # <-- Note the capitalization!

# targetJar = '/dev/optimus-prime/code/columbugus-assembly-2.1.jar'
targetJar = '/Users/acflorea/phd/columbugus/target/scala-2.10/columbugus-assembly-2.1.jar'

# sparkLocation = '/root/ibm/spark-dk-1.6.3.0/spark/bin/spark-submit'
sparkLocation = '/Users/acflorea/Bin/spark-1.6.2-bin-hadoop2.6/bin/spark-submit'

# configFile = '/dev/optimus-prime/firefox/firefox.conf'
configFile = '/Users/acflorea/Bin/spark-1.6.2-bin-hadoop2.6/columbugus-conf/netbeans.conf'

# fsRoot = '/dev/optimus-prime/data/firefox'
fsRoot = '/Users/acflorea/phd/columbugus_data/netbeans_final_test'

numEvals = 3


def objectiveFunction(categoryScalingFactor, productScalingFactor,
                      stepSize=1, regParam=0.01, tuningMode=True):
    print "We begin..."

    resultsFileName = identifier + '_results.out'

    if (tuningMode):
        mode = 'true'
    else:
        mode = 'false'

    sparkParams = '-Dconfig.file=' + configFile + ' ' \
                                                  '-Dreccsys.phases.preprocess=true ' \
                                                  '-Dreccsys.preprocess.includeCategory=true ' \
                                                  '-Dreccsys.preprocess.includeProduct=true ' \
                                                  '-Dreccsys.global.tuningMode=' + mode \
                  + ' -Dreccsys.filesystem.resultsFileName=' + resultsFileName \
                  + ' -Dreccsys.filesystem.root=' + fsRoot \
                  + ' -Dreccsys.preprocess.categoryScalingFactor=' + str(categoryScalingFactor) \
                  + ' -Dreccsys.preprocess.productScalingFactor=' + str(productScalingFactor) \
                  + ' -Dreccsys.train.stepSize=' + str(stepSize) \
                  + ' -Dreccsys.train.regParam=' + str(regParam)

    call([sparkLocation,
          '--class', 'dr.acf.recc.ReccomenderBackbone',
          '--master=local[*]',
          '--executor-memory', '10G',
          '--driver-memory', '64G',
          '--driver-java-options',
          '-Xmx80G',
          '--driver-java-options',
          sparkParams,
          targetJar])

    f = open(fsRoot + "/" + resultsFileName, 'r')
    # the results are in this form 'P:0.7624192322289902 R:0.6971544715447155 F:0.6995586152582066'
    results = f.read().split(' ')

    print results
    print "And we're done!"

    return float(results[2][2:])


# Go!
# objectiveFunction(categoryScalingFactor=1, productScalingFactor=1)

solvers = {'particle swarm': 'ps', 'nelder-mead': 'nm', 'random search': 'rnd', 'grid search': 'g'}

for algorithm, identifier in solvers.iteritems():
    print("*" * 80)
    print("RUN - " + algorithm)
    print("*" * 80)

    optimap_params, info, _ = optunity.maximize(objectiveFunction,
                                                num_evals=numEvals,
                                                categoryScalingFactor=[0, 120],
                                                productScalingFactor=[0, 120],
                                                # stepSize=[0.8, 1.2],
                                                # regParam=[0.005, 0.015],
                                                solver_name=algorithm)

    print("Optimal parameters: " + str(optimap_params))
    print("F1 of tuned model : %1.3f" % info.optimum)

    df = optunity.call_log2dataframe(info.call_log)
    df.to_csv(identifier + '_out.csv')

    # cutoff = 0.5
    # fig = plt.figure()
    # ax = Axes3D(fig)

    # ax.scatter(xs=df[df.value > cutoff]['categoryScalingFactor'],
    #           ys=df[df.value > cutoff]['productScalingFactor'],
    #           zs=df[df.value > cutoff]['value'])
    # ax.set_xlabel('categoryScalingFactor')
    # ax.set_ylabel('productScalingFactor')
    # ax.set_zlabel('F1')

    # plt.show()

    print("*" * 80)
    print("DONE - " + algorithm)
    print("*" * 80)
