# gtsperf
During the course of our Research Project we will evaluate the performance of various Docker overlay solutions in a high latency environment. To simulate such an environment the GÉANT Testbeds Service (GTS) will be utilized. The DSL file included in this repository generates the full mesh environment which will be used during the course of the project. 
![alt tag](https://raw.githubusercontent.com/siemhermans/gtsperf/master/GTS/Mesh.png)

IP-addresses are assigned by 192.168.[link nr.].[host nr.]/24.

Overlay solutions to be tested are Weave Net, Project Calico and Flannel as of now. For each of the overlay solutions a subfolder has been generated. The main script in the repository provides all options to deploy an overlay (master or slave) for each of the solutions. 
