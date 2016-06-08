# -*- coding: utf-8 -*-
"""
Author: Arne Zismer
Date: 8-6-2016
Project: Performance of Docker overlay networks
Usage: python measureDatagramEffect.py <overlay-name> <iperf3-server-IP> <interface>
Description: This script measures the TCP throughput, packet loss and CPU usage
             of connections with different window sizes. The measured results and the
             created plots are stored in the "result" folder created by this script.
             All measurements are taken 20 times.
             This script requires a running instance of iperf3 server on the
             target IP address.
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
    """
    Prints the 'message' to the screen and logs it to a logfile
    """

    print message
    log.info(message)


def cleanDataDir(dataDir):
    """
    Removes the given directory and all its subfolders and contained files
    """

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


def runTests(testRepetitions, repInterval, dataDir, windowSizes, overlayNetwork,
             serverAddr, duration):
    """
    Measures the TCP throughput for different window sizes.
    'repInterval' can be used to define the time to sleep between each iteration
    The tests are repeated 'repInterval' times and all results are written to the 'dataDir'.
    """

    for rep in range(testRepetitions):
        printlog("Iteration: {0}/{1}".format(rep + 1, testRepetitions))
        startTime = time()

        repDir = path.join(dataDir, "test_repetition_{0}".format(rep))
        mkdir(repDir)

        # call iperf3 with different datagram sizes
        for windowSize in windowSizes:

            printlog("\tTCP Window size of {0} KBytes".format(windowSize / 1000))
            outputFile = open("{0}/iperf3_{1}_window_{2:07d}.json".format(repDir, overlayNetwork, windowSize),"w")
            result = call(["iperf3", "-J", "-c", serverAddr, "-t", duration, "-w", str(windowSize)], stdout=outputFile)
            outputFile.close()
            if result != 0:
                print "Iperf3 could not start. Is the server running? If so, try restarting it."
                exit(1)

            sleep(1)  # give iperf some time to restart

        # sleep until interval time is over
        testDuration = time() - startTime
        timeToSleep = repInterval - testDuration if repInterval - testDuration > 0 else 0
        sleep(timeToSleep)


def readTestData(dataDir):
    """
    Create separate plots of for throughput, CPU usage and retrasmits
    """

    # iterate over repetition directories
    throughputMatrix = array([])
    cpuMatrix = array([])
    retransmitMatrix = array([])
    for repetitionDir in [ path.join(dataDir, f) for f in sorted(listdir(dataDir))]:

        throughputs = array([])
        cpuUsages = array([])
        retransmitRates = array([])

        # iterate over TCP window results of each repetition
        for filePath in [ path.join(repetitionDir, f) for f in sorted(listdir(repetitionDir)) ]:

            # read file and extract throughput, CPU usage and retansmits
            resultFile = open(filePath)
            result = resultFile.read()
            jsonResult = json.loads(result)
            bitsPerSecond = float(jsonResult["end"]["sum_received"]["bits_per_second"])
            cpuUsage = float(jsonResult["end"]["cpu_utilization_percent"]["host_total"])
            transmittedBytes = float(jsonResult["end"]["sum_received"]["bytes"])
            retransmit = float(jsonResult["end"]["sum_sent"]["retransmits"])
            retransmitsPerMB = retransmit / (transmittedBytes * 1000000)

            # convert to Mbits/s and append
            throughputs = append(throughputs, bitsPerSecond / 1000000)
            cpuUsages = append(cpuUsages, cpuUsage)
            retransmitRates = append(retransmitRates, retransmitsPerMB)

        # add finished test to result matrix
        if len(throughputMatrix) == 0:
            throughputMatrix = throughputs
            cpuMatrix = cpuUsages
            retransmitMatrix = retransmitRates
        else:
            throughputMatrix = vstack((throughputMatrix, throughputs))
            cpuMatrix = vstack((cpuMatrix, cpuUsages))
            retransmitMatrix  = vstack((retransmitMatrix , retransmitRates))

    return {"throughput": throughputMatrix, "CPU":  cpuMatrix, "retransmits": retransmitMatrix}


def plotThroughputAsBarChart(resultMatrix, overlayNetwork, windowsSizes):
    """
    Calculates means and variance of throughput result matrix and draws plot
    """

    printlog("Plotting throughput ...")

    # calculate mean and standard deviation of
    means = resultMatrix.mean(axis=0)
    deviations = resultMatrix.std(axis=0)

    # plot throughput per Window Size
    plt.subplots_adjust(bottom=0.2)
    plt.title(overlayNetwork)
    plt.bar(arange(len(means)), means, width=0.8, color="green", yerr=deviations)
    plt.xlim([0, len(means)])
    plt.xticks(arange(len(windowsSizes)) + 0.4, windowsSizes / 1000, rotation=45)
    plt.xlabel(r"TCP window size in KBytes", fontsize=12)
    plt.ylim([0, 300])
    plt.ylabel(r"Throughput in Mbits/s", fontsize=12)
    plt.savefig("result/TCPwindow_throughput_{0}.png".format(overlayNetwork))
    #plt.show()


def plotCPUAsBarChart(resultMatrix, overlayNetwork, windowsSizes):
    """
    Calculates means and variance of CPU usage result matrix and draws plot
    """

    printlog("Plotting CPU usage ...")

    # calculate mean and standard deviation of
    means = resultMatrix.mean(axis=0)
    deviations = resultMatrix.std(axis=0)

    # plot CPU usage per Window Size
    plt.subplots_adjust(bottom=0.2)
    plt.title(overlayNetwork)
    plt.bar(arange(len(means)), means, width=0.8, color="green", yerr=deviations)
    plt.xlim([0, len(means)])
    plt.xticks(arange(len(windowsSizes)) + 0.4, windowsSizes / 1000, rotation=45)
    plt.xlabel(r"TCP window size in KBytes", fontsize=12)
    plt.ylim([0, 100])
    plt.ylabel(r"Total host CPU usage in %", fontsize=12)
    plt.savefig("result/TCPwindow_CPU_{0}.png".format(overlayNetwork))
    #plt.show()


def plotRetransmitsAsBarChart(resultMatrix, overlayNetwork, windowsSizes):
    """
    Calculates means and variance of retransmits result matrix and draws plot
    """

    printlog("Plotting retransmits ...")

    # calculate mean and standard deviation of
    means = resultMatrix.mean(axis=0)
    deviations = resultMatrix.std(axis=0)

    # plot retransmits per Window Size
    plt.subplots_adjust(bottom=0.2)
    plt.title(overlayNetwork)
    plt.bar(arange(len(means)), means, width=0.8, color="green", yerr=deviations)
    plt.xlim([0, len(means)])
    plt.xticks(arange(len(windowsSizes)) + 0.4, windowsSizes / 1000, rotation=45)
    plt.xlabel(r"TCP window size in KBytes", fontsize=12)
    plt.ylim([0, 100])
    plt.ylabel(r"Retransmits / received MByte", fontsize=12)
    plt.savefig("result/TCPwindow_retransmits_{0}.png".format(overlayNetwork))
    #plt.show()


def setupLogging(logFileName):
    """
    Creates a log object which logs a message to file, including a timestamp
    """

    # setup logger
    log = logging.getLogger('TCP Window Log')
    log.setLevel(logging.INFO)

    # set rotation behaviour
    handler = RotatingFileHandler(logFileName, maxBytes=5000, backupCount=0)

    # set format
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    log.addHandler(handler)

    return log

if __name__ == "__main__":

    testRepetitions = 2  # default 20
    repInterval = -1   # 3360
    duration = "120"       # 120
    dataDir = "Window_testdata"
    logFileName = "WindowTest.log"

    # setup logging
    log = setupLogging(logFileName)

    # make sure program is started with valid arguments
    if (len(argv) < 3):
        print "Invalid arguments. Run like this:"
        print "python {0} <overlay-name> <iperf3-server-address>".format(argv[0])
        exit(1)

    overlayNetwork = argv[1]
    serverAddr = argv[2]
    printlog("Running on {0} overlay. Connecting to address {1}".format(
        overlayNetwork, serverAddr))

    windowSizes = array([2000, 4000, 8000, 16000, 32000, 64000, 128000, 256000, 512000, 1024000])

    # make sure dataDir exists and is empty
    cleanDataDir(dataDir)

    # run tests
    runTests(testRepetitions, repInterval, dataDir, windowSizes, overlayNetwork,
             serverAddr, duration)

    # read throughput of all results
    testResults = readTestData(dataDir)

    # make sure result directory exists
    if not path.isdir("result"):
        mkdir("result")

    # plot results
    plotThroughputAsBarChart(testResults["throughput"], overlayNetwork, windowSizes)
    plotCPUAsBarChart(testResults["CPU"], overlayNetwork, windowSizes)
    plotRetransmitsAsBarChart(testResults["retransmits"], overlayNetwork, windowSizes)
    printlog("Performance test finished!")














