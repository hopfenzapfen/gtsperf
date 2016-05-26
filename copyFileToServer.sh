#!/bin/bash




if [ $# -ne 1 ]; then
	echo "Please give a file name"
	exit 1
fi
FILENAME=$1

echo "Copying '${FILENAME}' to the servers"

for IP in 172.16.0.28 172.16.0.24 172.16.0.29 172.16.0.30
do
	scp $FILENAME gts@$IP:
done

echo "Done"