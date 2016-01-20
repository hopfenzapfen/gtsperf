The Dockerfile in this directory includes common performance measurement tools like iperf 2.0.5, iperf 3.0.11 and netperf 2.6.0. In order to perform any measurements, the container has to be built with 'docker build'. After creating the image, a measurement can be invoked by specifying either of the following commands:

``` docker run -e MODE="SERVER" 33b1807aec46  ```

```docker run -e MODE="CLIENT" -e TEST="IPERF" -e TYPE="TCP" -e SRCSITE="AMS" -e DSTSITE="PRG" -e ADDRESS="172.17.0.2" -e OVERLAY="NONE" -v /data 33b1807aec46```

In order to perform measurements with iperf, first a server container has to be spun up. This can be done with 
 Roderick W. Smith
