# -*- coding: utf-8 -*-
"""
Author: Arne Zismer
Date: 8-6-2016
Project: Performance of Docker overlay networks
Usage: python measureCPUeffect.py <overlay name> <iperf3-server-IP> <UDP or TCP>
Description: This script measures the UDP or TCP throughput using iperf3 and uses
             stress-ng to create additional CPU workload for different
             portions of the measurement time. All measurement results and the
             created files are stored in the "result" folder created by this script.
             The test is repeated 20 times.
             This script requires a running instance of iperf3 server on the
             target IP address.
"""

from sys import argv
from time import sleep, time
from subprocess import call, Popen
from numpy import arange, array, append, vstack
from os import mkdir, path, listdir, remove, devnull
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

    # print and log message
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


def runTests(dataDir, iterations, iperfDuration, bandwidth, cpuPercentages,
             repInterval, protocol):
    """
    Stresses the CPU for different percentages of time time that iperf3 is runninig
    and measures the throughput.
    These percentages are defined in the 'cpuPercentages' list.
    The 'protocol' variable specifies whether UDP or TCP throughput is measured.
    'repInterval' can be used to define the time to sleep between each iteration
    The tests are repeated 'repInterval' times and all results are written to the 'dataDir'.
    """

    # run test several times
    cpuCount = "1"  # how many CPU should be stressed
    delay = 2  # delay between starting stress-ng and starting iperf3
    stressDuration = iperfDuration + 2 * delay
    testDuration = stressDuration + 2

    for iteration in range(iterations):
        printlog("Iteration: {0}/{1}".format(iteration + 1, iterations))
        iterationStart = time()

        repDir = path.join(dataDir, "test_repetition_{0}".format(iteration))
        mkdir(repDir)

        for percentage in cpuPercentages:
            stressing = stressDuration * percentage
            printlog("\tStressing {0}/{1} seconds on {2} CPU(s)".format(stressing, iperfDuration, cpuCount))
            testStart = time()

            # start stressing CPU
            if stressing > 0:
                Popen(["stress-ng", "-c", str(cpuCount),
                      "-t", str(stressing)], stdout=open(devnull, 'w'))

            # give stress-ng some time to start up
            sleep(delay)

            # start iperf3
            outputFile = open("{0}/iperf3_{1}_CPU{2}.json".format(repDir, overlayNetwork,
                              percentage),"w")
            result = 1
            if protocol == "UDP":
                result = call(["iperf3", "-u", "-J", "-c", serverAddr, "-b",
                               bandwidth, "-t", str(iperfDuration)], stdout=outputFile)
            elif protocol == "TCP":
                result = call(["iperf3", "-J", "-c", serverAddr, "-t", str(iperfDuration)], stdout=outputFile)
            if result != 0:
                printlog("Iperf3 could not start. Is the server running? If so, try restarting it.")
                exit(1)

            # give stress-ng some time to stop
            timePassed = time() - testStart
            timeToSleep = testDuration - timePassed if testDuration - timePassed > 0 else 0
            sleep(timeToSleep)

        # sleep until next iteration starts (but last iterations shouldn't wait)
        if (iteration + 1 < iterations):
            iterationTime = time() - iterationStart
            timeToNextIteration = repInterval - iterationTime if repInterval - iterationTime > 0 else 0
            sleep(timeToNextIteration)


def setupLogging(logFileName):
    """
    Creates a log object which logs a message to file, including a timestamp
    """

    # setup logger
    log = logging.getLogger('MTU Log')
    log.setLevel(logging.INFO)

    # set rotation behaviour
    handler = RotatingFileHandler(logFileName, maxBytes=5000, backupCount=0)

    # set format
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    log.addHandler(handler)
    return log


def readTestData(dataDir, protocol):
    """
    Reads all the test data from the files and stacks them to a matrix
    """

    # iterate over repetition directories
    printlog("reading test data ...")
    resultMatrix = array([])
    for repetitionDir in [ path.join(dataDir, f) for f in sorted(listdir(dataDir))]:

        throughputs = array([])

        # iterate over CPU results of each repetition
        for filePath in [ path.join(repetitionDir, f) for f in sorted(listdir(repetitionDir)) ]:

            # read file and extract throughput
            resultFile = open(filePath)
            result = resultFile.read()
            jsonResult = json.loads(result)
            bitsPerSecond = 0
            if (protocol == "UDP"):
                bitsPerSecond = float(jsonResult["end"]["sum"]["bits_per_second"])
            elif (protocol == "TCP"):
                bitsPerSecond = float(jsonResult["end"]["sum_received"]["bits_per_second"])


            # convert to Mbits/s and append
            throughputs = append(throughputs, bitsPerSecond / 1000000)

        # add finished test to result matrix
        if len(resultMatrix) == 0:
            resultMatrix = throughputs
        else:
            resultMatrix = vstack((resultMatrix, throughputs))

    return resultMatrix


def plotResultsAsBarChart(resultMatrix, overlayNetwork, cpuPercentages, protocol):
    """
    Calculates means and variance of result matrix and draws plots
    """

    printlog("creating plot ...")

    # calculate mean and standard deviation of
    means = resultMatrix.mean(axis=0)
    deviations = resultMatrix.std(axis=0)

    # plot throughput per MTU
    plt.subplots_adjust(bottom=0.2)
    plt.title(overlayNetwork)
    plt.bar(arange(len(means)), means, width=0.8, yerr=deviations, \
            color="#005DE0", alpha=0.8, ecolor="#000000")
    plt.xlim([0, len(means)])
    plt.xticks(arange(len(cpuPercentages)) + 0.4, (cpuPercentages * 100).astype(int), rotation=45)
    plt.xlabel(r"Simultaneous CPU stressing in % of total measuring time", fontsize=12)
    plt.ylim([0, 360])
    plt.ylabel(r"{0} throughput in Mbits/s".format(protocol), fontsize=12)
    plt.savefig("result/CPU_{0}.png".format(overlayNetwork))
    plt.show()


if __name__ == "__main__":

    cpuPercentages = arange(0, 1.2, 0.2)  # default: 0, 1.2, 0.2
    iterations = 20  # 20
    repInterval = 1800  # 1800
    iperfDuration = 120  # 120
    bandwidth = "1000M"  # 1000M  just for UDP
    dataDir = "CPU_testdata"
    logFileName = "CPUtest.log"

    # setup logging
    log = setupLogging(logFileName)

    # check if stress-ng is installed and added to search path
    if call(["which", "stress-ng"], stdout=open(devnull, 'w')) != 0:
        printlog("stress-ng not found. Is it installed and added to the search path?")
        exit(1)

    # make sure program is started with valid arguments
    if (len(argv) < 4 or argv[3] not in ["UDP", "TCP"]):
        printlog("Invalid arguments. Run like this:")
        printlog("python {0} <overlay-name> <iperf3-server-address> <Protocol: TCP or UDP>".format(argv[0]))
        exit(1)

    overlayNetwork = argv[1]
    serverAddr = argv[2]
    protocol = argv[3]
    dataDir = "{0}_{1}".format(dataDir, protocol)
    printlog("Running on {0} overlay. Connecting to address {1} using {2}".format(
        overlayNetwork, serverAddr, protocol))

    # make sure dataDir exists and is empty
    cleanDataDir(dataDir)

    # run tests
    runTests(dataDir, iterations, iperfDuration, bandwidth, cpuPercentages, repInterval, protocol)

    # read test data
    resultMatrix = readTestData(dataDir, protocol)

    # make sure result directory exists
    if not path.isdir("result"):
        mkdir("result")

    # plot results
    plotResultsAsBarChart(resultMatrix, overlayNetwork, cpuPercentages, protocol)

    printlog("Performance test finished!")