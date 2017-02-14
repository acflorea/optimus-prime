from subprocess import call, Popen, PIPE
import time
import glob
import os

key = "ParagraphVector"

folder = '/Users/acflorea/phd/mariana-triage/'
pingInterval = 10

maxEpochs = 50

sparkLocation = '/root/ibm/spark-dk-1.6.3.0/spark/bin/spark-submit'
# sparkLocation = '/Users/acflorea/Bin/spark-1.6.2-bin-hadoop2.6/bin/spark-submit'

sparkParams = '-Dconfig.file=./application.conf ' \
              '-Dmariana.global.sourceModel={0} ' \
              '-Dmariana.global.startEpoch={1} ' \
              '-Dprogram.key=' + key

targetJar = "/data/mariana-triage/code/mariana-triage-assembly-1.2.5.jar"


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
                       mostRecentModel.rfind('/') + 1:mostRecentModel.rfind('_')] + "_" + counter + ".zip"
        else:
            counter = 0
            newModel = ''
            print "No model found"

        call(["nohup", sparkLocation,
              '--class', 'dr.acf.experiments.ParagraphVector',
              '--master=local[5]',
              '--executor-memory', '25G',
              '--driver-memory', '128G',
              '--driver-java-options',
              '-Xmx156G',
              '--driver-java-options',
              sparkParams.format(newModel, counter),
              targetJar],
             stdout=open('./triage.out', 'w'),
             stderr=open('./triage.err', 'a'))

    time.sleep(pingInterval)
