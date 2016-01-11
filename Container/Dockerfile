FROM ubuntu:14.04
MAINTAINER Siem Hermans email: siem.hermans@os3.nl

WORKDIR /
# Update sources & install essential tools
RUN apt-get -qq update && apt-get install -yqq \
    wget \
    build-essential \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Install testing tools (iperf & netperf)
RUN wget https://iperf.fr/download/iperf_3.0/iperf3_3.0.11-1_amd64.deb https://iperf.fr/download/iperf_3.0/libiperf0_3.0.11-1_amd64.deb
RUN dpkg -i libiperf0_3.0.11-1_amd64.deb iperf3_3.0.11-1_amd64.deb && rm libiperf0_3.0.11-1_amd64.deb iperf3_3.0.11-1_amd64.deb
RUN wget ftp://ftp.netperf.org/netperf/netperf-2.7.0.tar.gz && tar -xzvf netperf-2.7.0.tar.gz
RUN cd netperf-2.7.0 &&./configure --enable-demo=yes && make && make install && rm ../netperf-2.7.0.tar.gz

# Expose the default ports, statically linked (iperf, netperf)
EXPOSE 5201:5201 12865:12865

#COPY ./performance.sh /
#ENTRYPOINT ["/performance.sh"]
#CMD [ "-D", "FOREGROUND" ]
