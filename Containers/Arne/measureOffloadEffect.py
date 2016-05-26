#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Created on Thu Apr 21 21:00:05 2016

@author: hopfenzapfen
"""
from sys import argv
from time import sleep, time
from subprocess import call
from numpy import arange, array, append, vstack
from os import mkdir, path, listdir, remove
from shutil import rmtree
import logging
from logging.handlers import RotatingFileHandler
import json
import matplotlib
matplotlib.use('Agg')  # otherwise plot cannot be created on server
from matplotlib import pyplot as plt


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


def setOffloading(interface, status):
    """
    Set TCP segmentation offloading of given interface to 'on' or 'off'
    """
    call(["ethtool", "-K", interface, "gso", status, "tso", status])


def runTests(testRepetitions, repInterval, dataDir, overlayNetwork, interface,
             serverAddr, duration):

    statuses = ["on", "off"]

    for rep in range(testRepetitions):
        printlog("Iteration: {0}/{1}".format(rep + 1, testRepetitions))
        startTime = time()

        repDir = path.join(dataDir, "test_repetition_{0}".format(rep))
        mkdir(repDir)

        for status in statuses:

            printlog("\tTCP Segmentation offload: {0}".format(status))
            setOffloading(interface, status)
            outputFile = open("{0}/iperf3_{1}_offload_{2}.json".format(repDir, overlayNetwork, status), "w")
            result = call(["iperf3", "-J", "-c", serverAddr, "-t", duration], stdout=outputFile)
            outputFile.close()
            if result != 0:
                print "Iperf3 could not start. Is the server running? If so, try restarting it."
                exit(1)

            sleep(1)  # give iperf some time to restart

        # sleep until interval time is over
        testDuration = time() - startTime
        timeToSleep = repInterval - testDuration if repInterval - testDuration > 0 else 0
        sleep(timeToSleep)

    setOffloading(interface, "on")


def readTestData(dataDir):
    """
    Read results and return mean and deviation for statuses
    """

    # iterate over repetition directories
    throughputMatrix = array([])
    for repetitionDir in [ path.join(dataDir, f) for f in sorted(listdir(dataDir))]:

        throughputs = array([])

        # iterate over TCP offload results of each repetition
        for filePath in [ path.join(repetitionDir, f) for f in sorted(listdir(repetitionDir)) ]:

            # read file and extract throughput, CPU usage and retansmits
            resultFile = open(filePath)
            result = resultFile.read()
            jsonResult = json.loads(result)
            bitsPerSecond = float(jsonResult["end"]["sum_received"]["bits_per_second"])

            # convert to Mbits/s and append
            throughputs = append(throughputs, bitsPerSecond / 1000000)

        # add finished test to result matrix
        if len(throughputMatrix) == 0:
            throughputMatrix = throughputs
        else:
            throughputMatrix = vstack((throughputMatrix, throughputs))

    # calculate mean and standard deviation
    means = throughputMatrix.mean(axis=0)
    deviations = throughputMatrix.std(axis=0)

    return {"offload off": {"mean": "{:.2f}".format(means[0]), "deviation": "{:.2f}".format(deviations[0])},
            "offload on": {"mean": "{:.2f}".format(means[1]), "deviation": "{:.2f}".format(deviations[1])}}

def setupLogging(logFileName):

    # setup logger
    log = logging.getLogger('TCP Offload Log')
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
    repInterval = 900   # 900
    duration = "120"   # 120
    dataDir = "Offload_testdata"
    logFileName = "OffloadTest.log"

    # setup logging
    log = setupLogging(logFileName)

    # make sure program is started with valid arguments
    if (len(argv) < 4):
        print "Invalid arguments. Run like this:"
        print "python {0} <overlay-name> <iperf3-server-address> <interface>".format(argv[0])
        exit(1)

    overlayNetwork = argv[1]
    serverAddr = argv[2]
    interface = argv[3]
    printlog("Running on {0} overlay. Connecting to address {1}".format(
        overlayNetwork, serverAddr))

    # make sure dataDir exists and is empty
    cleanDataDir(dataDir)

    # run tests
    runTests(testRepetitions, repInterval, dataDir, overlayNetwork, interface,
             serverAddr, duration)

    # read throughput of all results
    testResults = readTestData(dataDir)

    # make sure result directory exists
    if not path.isdir("result"):
        mkdir("result")

    # write output to file
    fileName = "result/result.json"
    printlog("writing results to {0}".format(fileName))
    with open(fileName, "w") as outputFile:
        json.dump(testResults, outputFile, indent=4)


    printlog("Results:\n{0}".format(json.dumps(testResults, indent=4)))
    printlog("Performance test finished!")














