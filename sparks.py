from subprocess import call

def targetFn():

    print "We begin..."

    resultsFileName = 'results.out'
    root = '/Users/acflorea/phd/columbugus_data/netbeans_final_test'

    sparkParams = '-Dconfig.file=/Users/acflorea/Bin/spark-1.6.2-bin-hadoop2.6/columbugus-conf/netbeans.conf ' \
              '-Dreccsys.phases.preprocess=false ' \
              '-Dreccsys.preprocess.includeCategory=false ' \
              '-Dreccsys.preprocess.includeProduct=false ' \
              '-Dreccsys.filesystem.resultsFileName=' + resultsFileName + ' -Dreccsys.filesystem.root=' + root

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
    results = f.read()
    print results

    print "And we're done!"

# Go!
targetFn()