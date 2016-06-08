# -*- coding: utf-8 -*-
"""
Author: Arne Zismer
Date: 8-6-2016
Project: Performance of Docker overlay networks
Usage: python measureDatagramEffect.py <overlay-name> <iperf3-server-IP> <interface>
Description: This script measures the UDP throughput of connections with different
             datagram sizes. For each datagram size, measurements are taken with
             and without UDP fragmentation offloading. The measured results and the
             created plots are stored in the "result" folder created by this script.
             All measurements are taken 20 times.
             This script requires a running instance of iperf3 server on the
             target IP address.
"""
from sys import argv
from time import sleep, time
from subprocess import call, Popen, check_output, PIPE
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


def getMTU(interface):
    """
    Extracts the MTU of the given interface from ifconfig
    """

    ps = Popen(["ifconfig", interface], stdout=PIPE)
    return int(check_output(("awk", "-F[: ]+", "/MTU:/ {print $7}"), stdin=ps.stdout))


def setOffloading(interface, status):
    """
    Set UDP fragmentation offloading of given interface to 'on' or 'off'
    """
    call(["ethtool", "-K", interface, "ufo", status])


def runTests(testRepetitions, repInterval, dataDir, datagramSizes, overlayNetwork,
             serverAddr, interface, bandwidth, duration):
    """
    Measures the UDP throughput for different datagram sizes with and without
    UDP fragmentation offloading.
    'repInterval' can be used to define the time to sleep between each iteration
    The tests are repeated 'repInterval' times and all results are written to the 'dataDir'.
    """

    # test with and without UDP fragmentation offloading
    statuses = ["off", "on"]
    for status in statuses:

        printlog("UDP fragmentation offload: {0}".format(status))
        setOffloading(interface, status)
        statusDir = path.join(dataDir, "UFO_{0}".format(status))
        mkdir(statusDir)

        # repeat test multiple times
        for rep in range(testRepetitions):
            printlog("Iteration: {0}/{1}".format(rep + 1, testRepetitions))
            startTime = time()

            repDir = path.join(statusDir, "test_repetition_{0}".format(rep))
            mkdir(repDir)

            # call iperf3 with different datagram sizes and write result to json file
            for datagramSize in datagramSizes:

                printlog("\tDatagram size of {0} bytes".format(datagramSize))
                outputFile = open("{0}/iperf3_{1}_datagram{2}.json".format(repDir, overlayNetwork, datagramSize),"w")
                result = call(["iperf3", "-u", "-J", "-c", serverAddr, "-b", bandwidth,
                      "-t", duration, "-l", str(datagramSize)], stdout=outputFile)
                outputFile.close()
                if result != 0:
                    print "Iperf3 could not start. Is the server running? If so, try restarting it."
                    exit(1)

                sleep(1)  # give iperf some time to restart

        # sleep until interval time is over
        testDuration = time() - startTime
        timeToSleep = repInterval - testDuration if repInterval - testDuration > 0 else 0
        sleep(timeToSleep)

    # switch offloading back on when test is finished
    setOffloading(interface, "on")


def readTestData(dataDir):
    """
    Reads all the test data from the files and stacks them to a matrix
    """

    # iterate over status directories (on, off) and their child directories
    index = 0
    results = []
    for statusDir in [ path.join(dataDir, f) for f in sorted(listdir(dataDir)) ]:

        statusResult = array([])

        for repetitionDir in [ path.join(statusDir, f) for f in sorted(listdir(statusDir))]:

            throughputs = array([])

            # iterate over MTU results of each repetition
            for filePath in [ path.join(repetitionDir, f) for f in sorted(listdir(repetitionDir)) ]:

                # read file and extract throughput
                resultFile = open(filePath)
                result = resultFile.read()
                jsonResult = json.loads(result)
                bitsPerSecond = float(jsonResult["end"]["sum"]["bits_per_second"])

                # convert to Mbits/s and append
                throughputs = append(throughputs, bitsPerSecond / 1000000)

            # add finished test to status results
            if len(statusResult) == 0:
                statusResult = throughputs
            else:
                statusResult = vstack((statusResult, throughputs))

        # add status result to result matrix
        results.append(statusResult)
        index += 1

    return results


def plotResultsAsBarChart(results, overlayNetwork, datagramSizes):
    """
    Calculates means and variance of result matrix and draws plots
    """

    offloadOffResults = results[0]
    offloadOnResults = results[1]

    # calculate mean and standard deviation of throughputs
    meansOff = offloadOffResults.mean(axis=0)
    deviationsOff = offloadOffResults.std(axis=0)

    meansOn = offloadOnResults.mean(axis=0)
    deviationsOn = offloadOnResults.std(axis=0)

    # plot throughput per MTU
    barWidth = 0.3
    error_config = {'ecolor': '0.3'}
    plt.subplots_adjust(bottom=0.2)
    plt.title(overlayNetwork)
    if overlayNetwork.upper() != "VM":
        plt.bar(arange(len(meansOn)) - barWidth, meansOn, width=barWidth, error_kw=error_config, alpha=0.5,
                color="green", yerr=deviationsOn, label="offload enabled")
    plt.bar(arange(len(meansOff)), meansOff, width=barWidth, error_kw=error_config,
            color="red", yerr=deviationsOff, label="offload disabled")
    plt.xlim([-0.5, len(meansOff)])
    plt.xticks(arange(len(datagramSizes)), datagramSizes, rotation=45)
    plt.xlabel(r"Datagram size in bytes", fontsize=12)
    plt.ylim([0, 350])
    plt.ylabel(r"Throughput in Mbits/s", fontsize=12)
    plt.legend(loc="best")
    plt.savefig("result/datagram_{0}.png".format(overlayNetwork))
    plt.clf()
    #plt.show()


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

if __name__ == "__main__":

    testRepetitions = 20  # default 20
    repInterval = -1   # 3360
    duration = "120"       # 120
    bandwidth = "1000M"   # 1000M
    dataDir = "Datagram_Offloading_testdata"
    logFileName = "DatagramTest.log"

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
    mtu = getMTU(interface)
    printlog("Running on {0} overlay. Connecting to address {1}. MTU of interface {2} is {3}".format(
        overlayNetwork, serverAddr, interface, mtu))

    # generate datagram sizes dependent on MTU and VM or Docker
    stepSize = mtu - 28
    datagramSizes = array([])
    if overlayNetwork.upper() == "VM":
        datagramSizes = arange(stepSize, 11000, stepSize + 8)
    else:
        datagramSizes = arange(stepSize, 11000, stepSize - 4)

    # make sure dataDir exists and is empty
    cleanDataDir(dataDir)

    # run tests
    runTests(testRepetitions, repInterval, dataDir, datagramSizes, overlayNetwork,
             serverAddr, interface, bandwidth, duration)

    # read throughput of all results
    resultMatrix = readTestData(dataDir)

    # make sure result directory exists
    if not path.isdir("result"):
        mkdir("result")

    # plot results
    plotResultsAsBarChart(resultMatrix, overlayNetwork, datagramSizes)

    printlog("Performance test finished!")
