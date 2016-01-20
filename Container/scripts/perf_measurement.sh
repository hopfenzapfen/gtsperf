#!/bin/bash

if [[ $MODE =~ ^(client|CLIENT)$ ]]; then
  # netperf measurement
    # Generate timestamp
    psstart=$(date "+ %m/%d/%y %H:%M:%S:%3N")
    psend=$(date "+ %m/%d/%y %H:%M:%S:%3N")
    # Run performance measurement
    psresult=$(netperf -H 127.0.0.1 -t TCP_RR -- -O min_latency,mean_latency,p99_latency,stddev_latency | tail -n 1 | awk '{$1=$1}1' OFS=",")
    # Write log to file
    echo $psstart","$psend",AMS,LJU," $psresult
  # iperf measurement
    iperf -c $ADDRESS 
else
    iperf -s -D
    netserver
fi



