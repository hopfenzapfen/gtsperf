#!/bin/bash

if [ $# -ne 1 ]; then
	echo "Use script like this: $0 <path to file>"
	exit 1
fi
FILENAME=$1

VM1=172.16.0.13
VM2=172.16.0.10
VM3=172.16.0.12
VM4=172.16.0.15
VM5=172.16.0.11
VM6=172.16.0.14

echo "Copying '${FILENAME}' to the servers"

for IP in $VM1 $VM2 $VM3 $VM4 $VM5 $VM6
do
	scp $FILENAME gts@$IP:
done

echo "Done"