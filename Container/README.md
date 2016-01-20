#### Measurements
The Dockerfile in this directory includes common performance measurement tools like iperf 2.0.5, iperf 3.0.11 and netperf 2.6.0. In order to perform any measurements, the container has to be built with 'docker build'. When building the container, Docker pulls the official Ubuntu image from the Docker hub. In reality, this image is a very cut-down version of the original distribution with exclusively the bare runtime components required to run. During the course of the project, Ubuntu was used as the distribution of choice within the virtual environmenst as well as the containers because it is commonly available in IaaS environments. Furthermore, Ubuntu forms a common ground for all the tested overlay solutions with sufficient amounts of documentation available.

It should be noted that a patch is included in the Dockerfile for iperf 2.0.5. This patch, courtesy of Roderick W. Smith, fixes a bug that causes iperf on Linux to consume 100% CPU at the end of a run when it's run in daemon mode (e.g., "iperf -sD"). After running a measurement against the iperf daemon, the process would remain at 100% CPU utilization. Subsequent measurements would cause the server in question to quickly be brought to its knees. 

After creating the image, a measurement can be invoked by specifying either of the following commands:

All measurement tools require a server component to be active and running on the opposing site. When running the first command, a netperf server gets started and iperf daemons for both UDP and TCP communication are invoked. The $IMAGE_ID variable refers to the identifier of the image created by the 'docker build' command. 

``` docker run -e MODE="SERVER" $IMAGE_ID  ```

```docker run -e MODE="CLIENT" -e TEST="IPERF" -e TYPE="TCP" -e SRCSITE="AMS" -e DSTSITE="PRG" -e ADDRESS="172.17.0.2" -e OVERLAY="NONE" -v /data $IMAGE_ID ```

When the Docker container is invoked, a shell script is started to measure the performance between sites. This script reads environment variables from the container in order to decide which tool to use and which mode to apply. 

In order to perform measurements with iperf, first a server container has to be spun up. This can be done with 
 


This script reads ENV variables set by the Dockerfile by default. To
# override this behaviour, specify variables with docker run -e "VAR=value".
