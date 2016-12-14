from subprocess import call
import optunity


def objectiveFunction(categoryScalingFactor, productScalingFactor):
    print "We begin..."

    resultsFileName = 'results.out'
    root = '/Users/acflorea/phd/columbugus_data/netbeans_final_test'

    sparkParams = '-Dconfig.file=/Users/acflorea/Bin/spark-1.6.2-bin-hadoop2.6/columbugus-conf/netbeans.conf ' \
                  '-Dreccsys.phases.preprocess=true ' \
                  '-Dreccsys.preprocess.includeCategory=true ' \
                  '-Dreccsys.preprocess.includeProduct=true ' \
                  '-Dreccsys.filesystem.resultsFileName=' + resultsFileName \
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

pars, details, _ = optunity.maximize(objectiveFunction,
                                     num_evals=100,
                                     categoryScalingFactor=[0, 100],
                                     productScalingFactor=[0, 100],
                                     solver_name='grid search')

print pars