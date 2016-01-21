Architecture
============
The machines in GTS are deployed by OpenStack in KVM. 
GÉANT has Points of Presence (PoPs) in Amsterdam, Bratislava, Ljubljana, Milan and Prague. The sites are connected via dedicated point-to-point circuits 10Gbps optical waves.  

The virtual machines use pci_passthrough
giving it full and direct access to the PCI device.
Ubuntu 14.04 default


Limitations
===========
In order to deploy the topologies, GÉANT has defined a Domain Specific Language (DSL) for describing testbed networks. The DSL description defines structure of the toplogoy and the constraints for each requested resource, i.e. the required attributes of the resource. During the course of the project the GTS v2.0 DSL grammar has been used to define the topologies. [GITHUB LINK]. This limited the topologies to so-called 'first generation' virtual networks. These networks are dynamically provisioned but remain static throughout their reservation. Changes in the topology require tearing down the entire testbed before reserving it again. Furthermore, the virtual machines deployed in GTS are relatively static in terms of performance; each machine has a single-core vCPU. Performance-wise, the only attribute which can be altered is the speed of the processor with the 'cpuSpeed' attribute. The default value for this attribute is a 2 gigahertz (GHz).   

The problem that occurs is that when running performance measurements with iperf3, the vCPU can't saturate the 1Gbps link. Even when scaling up the cpuSpeed to an arbitrarily high number, the speed of the processer gets capped at 2.5GHz by OpenStack. When a large number of nodes is aIncreasing the amount of cores per vCPU is not a documented attribute and as such does not seem to be a publicly available API call. 

During the course of the project the third version of GTS has been rolled out. The current version is v3.0.1. “Second generation” networks will deliver more advanced features such as dynamic in-site modification, i.e. the ability to modify an active network without tearing down the entire existing testbed instance 


Footnote: All sources are available at 

[SOURCE] http://services.geant.net/GTS/Resources/Documents/D6-2_D2-3-2_TaaS_v2%200.pdf
[SOURCE] http://services.geant.net/GTS/Resources/PublishingImages/Pages/Home/User_Guide_v2.0.pdf


The initial topology used during the project was a meshed environment in a single site. With this setup 

The initial setup was a full mesh becaues 