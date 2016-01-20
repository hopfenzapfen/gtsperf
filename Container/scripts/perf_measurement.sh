#!/bin/bash
# This script reads ENV variables set by the Dockerfile by default. To
# override this behaviour, specify variables with docker run -e "VAR=value".
# Examples:
# docker run -e MODE="CLIENT" -e TEST="IPERF" -e TYPE="UDP" -e SRCSITE="AMS" -e DSTSITE="PRG" -e ADDRESS="172.17.0.2" -e OVERLAY="NONE" -v /data 18c2d4864eb3
# docker run -e MODE="SERVER" $IMAGE_ID

# Get the IP address of the machine
ifconfig

if [[ $MODE == "CLIENT" ]]; then
	# netperf measurement
	if [[ $TEST == "NETPERF" ]]; then
		# Generate timestamp (start)
		psstart=$(date +%Y%m%d%H%M%S)

		# Run performance measurement
		psresult=$(netperf -l 115 -H $ADDRESS -t TCP_RR -- -O min_latency,mean_latency,p99_latency,stddev_latency | tail -n 1 | awk '{$1=$1}1' OFS=",")

		# Generate timestamp (end)
		psend=$(date +%Y%m%d%H%M%S)

		# Write log to file
		echo $psstart","$psend","$OVERLAY","$SRCSITE","$DSTSITE","$psresult >> /data/'MSMT_'$SRCSITE'_'$DSTSITE'_'$TEST'_'$OVERLAY'.csv'

	elif [[ $TEST == "IPERF" ]]; then
		# Differentiate between TCP and UDP bandwith test
		if [[ $TYPE == "UDP" ]]; then
			# Run performance measurement & write to CSV
			iperf -c $ADDRESS -u -p 5002 -b 1000M -y C -t 155 | tail -n 1 >> /data/'MSMT_'$SRCSITE'_'$DSTSITE'_'$TEST'_'$TYPE'_'$OVERLAY'.csv'

		elif [[ $TYPE == "TCP" ]]; then
			# Run performance measurement & write to CSV
			iperf -c $ADDRESS -p 5001 -y C -t 155 >> /data/'MSMT_'$SRCSITE'_'$DSTSITE'_'$TEST'_'$TYPE'_'$OVERLAY'.csv'
		fi
	fi

else
    # Enter server condition if the $MODE =! client
	netserver
	# Run server as daemon mode
	iperf -s -D -p 5001
	iperf -s -u -p 5002
fi
