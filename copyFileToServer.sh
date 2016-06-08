#!/bin/bash

if [ $# -ne 1 ]; then
	echo "Use script like this: $0 <path to file>"
	exit 1
fi
FILENAME=$1

VM1=172.16.0.25
VM2=172.16.0.27
VM3=172.16.0.26
VM4=172.16.0.28

echo "Copying '${FILENAME}' to the servers"

for IP in $VM1 $VM2 $VM3 $VM4
do
	scp $FILENAME gts@$IP:
done

echo "Done"