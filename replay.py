from subprocess import call, Popen, PIPE
import time
import glob
import os
import shutil

pingInterval = 10

maxEpochs = 50

sparkLocation = '/root/ibm/spark-dk-1.6.3.0/spark/bin/spark-submit'
sparkLocation = '/Users/acflorea/Bin/spark-1.6.2-bin-hadoop2.6/bin/spark-submit'

configsLocation = '/Users/acflorea/phd/optimus-prime/configs/'

dbs = ["netbeans", "eclipse", "firefox_new"]
trainBatchSizes = [5, 10, 20, 30, 50, 100]
averagingFrequencies = [1, 5, 10, 20, 50]
workersList = [1, 4, 8, 12, 16]

targetJar = "/data/mariana-triage/code/mariana-triage-assembly-1.3.0.jar"
targetJar = "/Users/acflorea/phd/mariana-triage/target/scala-2.10/mariana-triage-assembly-1.3.0.jar"


# finds a pid based on a search key
def findProcess(key):
    ps = Popen("ps -ef | grep " + key + " | grep -v grep | awk '{print $2}'", shell=True, stdout=PIPE)
    output = ps.stdout.read()
    ps.stdout.close()
    ps.wait()
    return output.split("\n")


# finds most recent saved "model" (from the OS perspective, a model is just a simple zip file)
def findMostRecentModel(folder):
    try:
        files = glob.iglob(os.path.join(folder, '*.zip'))
        return max(files, key=os.path.getctime)
    except ValueError:
        None


for db in dbs:
    for trainBatchSize in trainBatchSizes:  # trainBatchSize
        for averagingFrequency in averagingFrequencies:  # averagingFrequency
            for workers in workersList:

                key = '{0}_{1}_{2}_{3}'.format(db, trainBatchSize, averagingFrequency, workers)
                folder = "./" + key

                if os.path.exists(folder):

                    print folder + " exists. Skip!"

                else:

                    print "Creating folder " + folder
                    os.mkdir(folder)
                    dataFolder = configsLocation + db + '/data_rnn'
                    if os.path.exists(dataFolder):
                        print "Copy data folder from " + dataFolder
                        shutil.copytree(dataFolder, folder + '/data_rnn')

                    sparkParams = '-Dconfig.file={0}.conf ' \
                                  '-Dmariana.global.sourceModel={1} ' \
                                  '-Dmariana.global.startEpoch={2} ' \
                                  '-Dmariana.global.trainBatchSize={3} ' \
                                  '-Dmariana.global.averagingFrequency={4} ' \
                                  '-Dprogram.key=' + key

                    while True:
                        print "Here we go, searching for ParagraphVector"
                        pids = findProcess(key)
                        if (len(pids) > 1):
                            print "Hurray ... still running"
                        else:
                            # process has died - attempt to relaunch
                            print "Cant' find process, attempting to restart"
                            mostRecentModel = findMostRecentModel(folder)
                            if (mostRecentModel):
                                counter = mostRecentModel[mostRecentModel.rfind('_') + 1: -4]
                                if counter >= maxEpochs:
                                    # Stop at maxEpochs
                                    break
                                print "Most recent model is " + mostRecentModel + " Counter is " + counter
                                newModel = mostRecentModel[
                                           mostRecentModel.rfind('/') + 1:mostRecentModel.rfind(
                                               '_')] + "_" + counter + ".zip"
                            else:
                                counter = 0
                                newModel = ''
                                print "No model found"

                            formattedSparkParams = sparkParams.format(configsLocation + db, newModel, counter,
                                                                      trainBatchSize,
                                                                      averagingFrequency)

                            call(["nohup", sparkLocation,
                                  '--class', 'dr.acf.experiments.ParagraphVector',
                                  '--master=local[' + str(workers) + ']',
                                  '--executor-memory', '25G',
                                  '--driver-memory', '128G',
                                  '--driver-java-options',
                                  '-Xmx156G',
                                  '--driver-java-options',
                                  formattedSparkParams,
                                  targetJar],
                                 stdout=open(folder + '/triage.out', 'w'),
                                 stderr=open(folder + '/triage.err', 'a'),
                                 cwd=folder)

                        time.sleep(pingInterval)
