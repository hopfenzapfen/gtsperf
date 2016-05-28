# -*- coding: utf-8 -*-
"""
Created on Fri May 27 20:15:54 2016

@author: hopfenzapfen
"""


from time import sleep
from subprocess import call, Popen, check_output, PIPE
from numpy import arange, array, append, vstack, transpose, cumsum
from os import mkdir, path, listdir, remove
from shutil import rmtree
import logging
from logging.handlers import RotatingFileHandler
import json
import matplotlib
matplotlib.use('Agg')  # otherwise plot cannot be created on server
from matplotlib import pyplot as plt

LATENCY = "Latency"
UDP_TP = "UDP_throughput"
TCP_TP = "TCP_throughput"


def printlog(message):
    print message
    log.info(message)


def cleanDataDir(dataDir):

    # make sure data directory exists
    if not path.exists(dataDir) or not path.isdir(dataDir):
        mkdir(dataDir)

    # wipe content if it already exists
    else:
        for f in [path.join(dataDir, f) for f in listdir(dataDir)]:
            if (path.isdir(f)):
                rmtree(f)
            else:
                remove(f)


def runNetperfTest(testRepetitions, testDir, serverAddresses, duration, test):

    hops = 1
    for ip in serverAddresses:
        printlog("Testing latency: hops: {0}".format(hops))

        # open file to store all results for certain hop count
        with open("{0}/netperf_hop{1}.json".format(testDir, hops), "a") as outputFile:

            outputFile.write("[")
            for rep in range(testRepetitions):
                printlog("\tIteration: {0}/{1}".format(rep + 1, testRepetitions))

                # perform latency test
                ps = Popen(["netperf", "-l", duration, "-H", ip, "-t", "UDP_RR", "--",
                            "-O", "min_latency,mean_latency,p99_latency,stddev_latency"], stdout=PIPE)
                values = check_output(("tail", "-n", "1"), stdin=ps.stdout)

                # transform results to dictionnary
                result = values.split()
                resultDict = {}
                resultDict["min_latency"] = result[0]
                resultDict["mean_latency"] = result[1]
                resultDict["p99_latency"] = result[2]
                resultDict["stddev_latency"] = result[3]

                # write results to file
                json.dump(resultDict, outputFile, indent=4)

                if (rep + 1) < testRepetitions:
                    outputFile.write(",")

            outputFile.write("]")

        hops += 1


def runIperf3Test(testRepetitions, testDir, serverAddresses, duration, test):

    printlog("Testing {0}:".format(test))

    for rep in range(testRepetitions):
        printlog("\tIteration: {0}/{1}".format(rep + 1, testRepetitions))

        repDir = path.join(testDir, "test_{0}_repetition_{1}".format(test, rep))
        mkdir(repDir)

        hops = 1
        for ip in serverAddresses:
            printlog("\t\tHop {0}".format(hops))

            with open("{0}/iperf3_{1}_hop{2}.json".format(repDir, test, hops),"w") as outputFile:

                result = 0
                if test == UDP_TP:
                    result = call(["iperf3", "-u", "-J", "-c", ip, "-b", bandwidth,
                                   "-t", duration], stdout=outputFile)

                elif test == TCP_TP:
                    result = call(["iperf3", "-J", "-c", ip, "-t", duration], stdout=outputFile)

                else:
                    printlog("Invalid test specified: {0}".format(test))
                    exit(1)

                # check if iperf3 executed correctly
                if result != 0:
                    print "Iperf3 could not start. Is the server running? If so, try restarting it."
                    exit(1)

            hops += 1
            sleep(1)  # give iperf/netstat some time to restart


def runTests(testRepetitions, dataDir, serverAddresses, duration, tests):

    for test in tests:
        testDir = path.join(dataDir, "Hop_{0}".format(test))
        mkdir(testDir)

        # netperf test
        if test == LATENCY:
            runNetperfTest(testRepetitions, testDir, serverAddresses, duration, test)

        # iperf3 tests
        else:
            runIperf3Test(testRepetitions, testDir, serverAddresses, duration, test)


def readNetperfResults(testDir):

    testResult = array([])

    # iterate over files (there is one file per hop number)
    for hopFile in [ path.join(testDir, f) for f in sorted(listdir(testDir)) ]:
        latencies = array([])

        # read file and extract latencies
        resultFile = open(hopFile)
        result = resultFile.read()
        jsonResult = json.loads(result)

        # each file consists of n measurements
        for iteration in jsonResult:
            latencies = append(latencies, float(iteration["mean_latency"]) / 1000)

        # add finished test to status results
        if len(testResult) == 0:
            testResult = latencies
        else:
            testResult = vstack((testResult, latencies))

    return transpose(testResult)



def readIperf3Results(testDir, test):

    testResult = array([])
    for repetitionDir in [ path.join(testDir, f) for f in sorted(listdir(testDir)) ]:

        throughputs = array([])

        # iterate over hop results of each repetition
        for filePath in [ path.join(repetitionDir, f) for f in sorted(listdir(repetitionDir)) ]:

            # read file and extract throughput
            resultFile = open(filePath)
            result = resultFile.read()
            jsonResult = json.loads(result)

            bitsPerSecond = 0
            if (test == UDP_TP):
                bitsPerSecond = float(jsonResult["end"]["sum"]["bits_per_second"])
            else:
                bitsPerSecond = float(jsonResult["end"]["sum_received"]["bits_per_second"])

            # convert to Mbits/s and append
            throughputs = append(throughputs, bitsPerSecond / 1000000)

        # add finished test to status results
        if len(testResult) == 0:
            testResult = throughputs
        else:
            testResult = vstack((testResult, throughputs))

    return testResult




def readTestData(dataDir, tests):

    results = {}
    for test in tests:
        testDir = path.join(dataDir, "Hop_{0}".format(test))

        # netperf results
        if test == LATENCY:
            results[test] = readNetperfResults(testDir)

        # iperf3 results
        else:
            results[test] = readIperf3Results(testDir, test)

    return results


def plotResultsAsBarChart(resultDict, tests, cumulativeLatencies):

    # plot results per test
    for test in tests:

        results = resultDict[test]

        # calculate mean and standard deviation of throughputs
        means = results.mean(axis=0)
        deviations = results.std(axis=0)

        barWidth = 0.3
        error_config = {'ecolor': '0.3'}

        # plot netperf results
        if test == LATENCY:
            plt.title(test)
            plt.ylim([0, 200])
            plt.ylabel(r"Mean latency in ms", fontsize=12)

            plt.bar(arange(len(means)) - barWidth, means, width=barWidth, error_kw=error_config,
                    color="green", yerr=deviations, label="latencies per amount of hops")
            plt.bar(arange(len(means)), cumulativeLatencies, width=barWidth, error_kw=error_config,
                    color="red", label="cumulative latencies for each hop")
            plt.legend(loc="best")

            plt.xlim([-0.5, len(means)])
            plt.xticks(arange(len(means)), arange(1, len(means) + 1), rotation=45)
            plt.xlabel(r"Number of hops", fontsize=12)
            plt.savefig("result/test_{0}.png".format(test))
         #   plt.show()
            plt.clf()

        # plot iperf3 results
        else:
            plt.title(test)
            plt.bar(arange(len(means)) - barWidth / 2, means, width=barWidth, error_kw=error_config,
                    color="green", yerr=deviations)
            plt.ylim([0, 300])
            plt.ylabel(r"Throughput in Mbits/s", fontsize=12)

            plt.xlim([-0.5, len(means)])
            plt.xticks(arange(len(means)), arange(1, len(means) + 1), rotation=45)
            plt.xlabel(r"Number of hops", fontsize=12)
            plt.savefig("result/test_{0}.png".format(test))
           # plt.show()
            plt.clf()


def setupLogging(logFileName):

    # setup logger
    log = logging.getLogger('Hop Log')
    log.setLevel(logging.INFO)

    # set rotation behaviour
    handler = RotatingFileHandler(logFileName, maxBytes=5000, backupCount=0)

    # set format
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    log.addHandler(handler)

    return log

if __name__ == "__main__":

    testRepetitions = 20  # default 20
    duration = "120"       # 120
    bandwidth = "1000M"   # 1000M
    dataDir = "Hopping_testdata"
    logFileName = "HopTest.log"
    tests = [LATENCY, UDP_TP, TCP_TP]

    # define addresses here. More convenient than getting them from command line
    serverAddresses = ["10.40.0.1", "10.44.0.1", "10.36.0.1", "10.34.0.1", "10.46.0.1"]
    segmentLatencies = [21.75, 4.70, 41.58, 52.57, 40.63]
    cumulativeLatencies = cumsum(segmentLatencies)

    # setup logging
    log = setupLogging(logFileName)

    # make sure dataDir exists and is empty
    cleanDataDir(dataDir)

    # run tests
    runTests(testRepetitions, dataDir, serverAddresses, duration, tests)

    # read throughput of all results
    resultDict = readTestData(dataDir, tests)

    # make sure result directory exists
    if not path.isdir("result"):
        mkdir("result")

    # plot results
    plotResultsAsBarChart(resultDict, tests, cumulativeLatencies)

    printlog("Performance test finished!")

