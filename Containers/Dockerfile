# Docker image to measure effect of UDP datagram size on throughput
# Build command: docker build -t udp_test_img .
# docker run -id --name <name> -v /home/gts/Docker/result:/root/result --net=<network> udp_test_img
# 
# Install run this container on both hosts.
# Within the container run iperf3 as server on one host: 			iperf3 -s
# Within the container run the perf.py script on the other host:	python perf.py <overlayNetwork> <iperf3 server address>

FROM ubuntu:14.04
MAINTAINER Arne Zismer, <arne.zismer@student.uva.nl>
LABEL version="1.0"
LABEL role="Docker overlay network performance measurement"

# Set timezone
ENV TZ=CET

# Set correct directory
ENV dir /root
WORKDIR ${dir}

# Update sources & install essential tools and iperf 3
RUN apt-get -qq update && apt-get install -yq 	wget build-essential git software-properties-common make nano
RUN sudo add-apt-repository -y "ppa:patrickdk/general-lucid" && \
	apt-get -qq update && \
	apt-get install -yq iperf3

# set xterm in order to use nano
RUN export TERM=xterm

# install iperf
RUN apt-get install -yq iperf

# install netperf
RUN wget --no-check-certificate ftp://ftp.netperf.org/netperf/netperf-2.7.0.tar.gz && tar -xzvf netperf-2.7.0.tar.gz && \
	cd netperf-2.7.0 && ./configure --enable-demo=yes && make && make install && rm ../netperf-2.7.0.tar.gz

# install stress-ng and create link to search path
RUN wget http://kernel.ubuntu.com/~cking/tarballs/stress-ng/stress-ng-0.03.11.tar.gz && \
	tar zxf stress-ng-0.03.11.tar.gz && \
	rm stress-ng-0.03.11.tar.gz && \
	cd stress-ng-0.03.11 && \
	make && \
	cd $dir && \
	ln -s  ${dir}/stress-ng-0.03.11/stress-ng /usr/bin/stress-ng

# install python libraries (for testing performance and plotting results)
RUN apt-get install -yq python python-matplotlib python-numpy

# copy test scripts
# ADD measureDatagramEffect.py ${dir}/DatagramPerf.py
# ADD measureCPUeffect.py ${dir}/CPUperf.py
# ADD measureWindowEffect.py ${dir}/WindowPerf.py
# ADD measureOffloadEffect.py ${dir}/OffloadPerf.py

# Expose the default ports, statically linked (iperf TCP/UDP, iperf3, netperf)
EXPOSE 5001:5001 5002:5002 5201:5201 12865:12865
