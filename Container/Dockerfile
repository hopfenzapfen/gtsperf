# In order to write the logs to a file on the host, the container should be started as 
# 'docker run --name perf_meas -v /data $IMAGE_ID'. The $IMAGE_ID is the ID of the image
# built with this Dockerfile. To view the logs, the following command should be run
# docker inspect -f '{{range .Mounts}}{{.Source}}{{end}}' $CONTAINER_NAME .

FROM ubuntu:14.04
MAINTAINER Siem Hermans, <siem.hermans@os3.nl>
LABEL version="1.0"
LABEL role="Performance measurement"

# Set timezone
ENV TZ=UTC

# Default to server mode with iperf TCP test

# Set correct directory
ENV dir /root
WORKDIR ${dir}

# Update sources & install essential tools  
RUN apt-get -qq update && apt-get install -yqq \
  wget \
  build-essential \
  git \
  iperf

# Pull and build testing tools (iperf3 & netperf)
RUN wget --no-check-certificate https://iperf.fr/download/iperf_3.0/iperf3_3.0.11-1_amd64.deb https://iperf.fr/download/iperf_3.0/libiperf0_3.0.11-1_amd64.deb
RUN dpkg -i libiperf0_3.0.11-1_amd64.deb iperf3_3.0.11-1_amd64.deb && rm libiperf0_3.0.11-1_amd64.deb iperf3_3.0.11-1_amd64.deb
RUN wget --no-check-certificate ftp://ftp.netperf.org/netperf/netperf-2.7.0.tar.gz && tar -xzvf netperf-2.7.0.tar.gz
RUN cd netperf-2.7.0 && ./configure --enable-demo=yes && make && make install && rm ../netperf-2.7.0.tar.gz

# Install netperf binaries and clean up directories
RUN mv -t /usr/bin netperf-2.7.0/src/netperf netperf-2.7.0/src/netserver && rm -rf netperf-2.7.0/

# Install iperf (2)
WORKDIR ${dir}
RUN wget --no-check-certificate http://heanet.dl.sourceforge.net/project/iperf/iperf-2.0.5.tar.gz 
RUN tar -xzvf iperf-2.0.5.tar.gz && cd iperf-2.0.5/src

# Patch iperf 2.0.5 in order to fix the 100% utilization bug when running iperf as a daemon
ADD scripts/nomaxcpu.patch ${dir}/iperf-2.0.5/src/nomaxcpu.patch
WORKDIR ${dir}/iperf-2.0.5/src/
patch < nomaxcpu.patch && cd ..
./configure && make && make install && cp src/iperf /usr/bin/iperf

# Include netperf and iperf scripts
ADD scripts/perf_measurement.sh ${dir}/perf.sh
RUN chmod +x perf.sh

# Execute performance measurements
CMD ./perf.sh
#STOPSIGNAL SIGKILL

# Expose the default ports, statically linked (iperf TCP/UDP, iperf3, netperf)
EXPOSE 5001:5001 5002:5002 5201:5201 12865:12865
