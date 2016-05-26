#### Measurements
The Dockerfile includes common performance measurement tools like iperf 2.0.5, iperf 3.0.11 and netperf 2.6.0. In order to perform any measurements, the container has to be built with 'docker build'. When building the container, Docker pulls the official Ubuntu image from the Docker hub. In reality, this image is a very cut-down version of the original distribution with exclusively the bare runtime components required to run. During the course of the project, Ubuntu was used as the distribution of choice within the virtual environmenst as well as the containers because it is commonly available in IaaS environments. Furthermore, Ubuntu forms a common ground for all the tested overlay solutions with sufficient amounts of documentation available.

It should be noted that a patch is included in the Dockerfile for iperf 2.0.5. This patch, courtesy of Roderick W. Smith, fixes a bug that causes iperf on Linux to consume 100% CPU at the end of a run when it's run in daemon mode (e.g., "iperf -sD"). After running a measurement against the iperf daemon, the process would remain at 100% CPU utilization. Subsequent measurements would cause the server in question to quickly be brought to its knees. 

After creating an image from the Dockerfile, a container can be started by specyfing either of the following commands. 

``` docker run -e MODE="SERVER" $IMAGE_ID  ```

```docker run -e MODE="CLIENT" -e TEST="IPERF" -e TYPE="TCP" -e SRCSITE="AMS" -e DSTSITE="PRG" -e ADDRESS="172.17.0.2" -e OVERLAY="NONE" -v /data $IMAGE_ID ```

All measurement tools in the container follow a client-server model and require a server component to be active and running on the opposing site. When running the first command, a netperf server gets started and iperf daemons for both UDP and TCP communication are invoked. The $IMAGE_ID variable refers to the identifier of the image created by the 'docker build' command. The '-e' in the command flag denotes an environment variable. These variables are used in the performance measurement script to differentiate between client and server mode, the type of measurement (TCP or UDP) and the available tools. The full set of environment variables is displayed in the latter command and includes logging specific variables like the source and destination site (for point-to-point measurements) and the specific overlay used. 

Lastly, the client command includes a '-v' flag with an arbitrary directory. This directory is shared with the host of the container and is used to write logging data to. Data written to this directory can be found by issuing the command below. Data will be available as long as the container is present on the machine, even when it enters an exited state. 

``` cd `docker inspect -f '{{range .Mounts}}{{.Source}}{{end}}' $CONTAINER_NAME` ```


