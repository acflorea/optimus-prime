from subprocess import call
import optunity

from matplotlib import pylab as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D  # <-- Note the capitalization!


def objectiveFunction(categoryScalingFactor, productScalingFactor, tuningMode=True):
    print "We begin..."

    resultsFileName = 'results.out'
    root = '/Users/acflorea/phd/columbugus_data/netbeans_final_test'

    if (tuningMode):
        mode = 'true'
    else:
        mode = 'false'

    sparkParams = '-Dconfig.file=/Users/acflorea/Bin/spark-1.6.2-bin-hadoop2.6/columbugus-conf/netbeans.conf ' \
                  '-Dreccsys.phases.preprocess=true ' \
                  '-Dreccsys.preprocess.includeCategory=true ' \
                  '-Dreccsys.preprocess.includeProduct=true ' \
                  '-Dreccsys.global.tuningMode=' + mode \
                  + ' -Dreccsys.filesystem.resultsFileName=' + resultsFileName \
                  + ' -Dreccsys.filesystem.root=' + root \
                  + ' -Dreccsys.preprocess.categoryScalingFactor=' + str(categoryScalingFactor) \
                  + ' -Dreccsys.preprocess.productScalingFactor=' + str(productScalingFactor)

    call(['/Users/acflorea/Bin/spark-1.6.2-bin-hadoop2.6/bin/spark-submit',
          '--class', 'dr.acf.recc.ReccomenderBackbone',
          '--master=local[*]',
          '--executor-memory', '20G',
          '--driver-java-options',
          '-Xmx32G',
          '--driver-java-options',
          sparkParams,
          '/Users/acflorea/phd/columbugus/target/scala-2.10/columbugus-assembly-2.1.jar'])

    f = open(root + "/" + resultsFileName, 'r')
    # the results are in this form 'P:0.7624192322289902 R:0.6971544715447155 F:0.6995586152582066'
    results = f.read().split(' ')

    print results
    print "And we're done!"

    return float(results[2][2:])


# Go!
# objectiveFunction(categoryScalingFactor=1, productScalingFactor=1)

optimap_params, info, _ = optunity.maximize(objectiveFunction,
                                            num_evals=100,
                                            categoryScalingFactor=[60, 120],
                                            productScalingFactor=[60, 120],
                                            solver_name='particle swarm')

print("Optimal parameters: " + str(optimap_params))
print("F1 of tuned model : %1.3f" % info.optimum)

df = optunity.call_log2dataframe(info.call_log)

cutoff = 0.5
fig = plt.figure()
ax = Axes3D(fig)

ax.scatter(xs=df[df.value > cutoff]['categoryScalingFactor'],
           ys=df[df.value > cutoff]['productScalingFactor'],
           zs=df[df.value > cutoff]['value'])
ax.set_xlabel('categoryScalingFactor')
ax.set_ylabel('productScalingFactor')
ax.set_zlabel('F1')

plt.show()
