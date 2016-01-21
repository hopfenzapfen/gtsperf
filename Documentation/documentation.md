### Docker
## Project
It has a single binary, docker, that can act as both client and server. As a client, the docker binary passes requests to the Docker daemon (e.g., asking it to return information about itself), and then processes those requests when they are returned. 

## Containers
AUTHOR defines containres as follows: A Docker container is an image format that can contain a set of standard operations and can function as an execution environment. Container technology allows multiple isolated user space instances to be run on a single host.they can generally only run the same or a similar guest operating system as the underlying host. Unlike traditional virtualization or paravirtualization technologies, they do not require an emulation layer or a hypervisor layer to run and instead use the operating system's normal system call interface.

They make excellent sandboxes for a variety of testing purposes. Additionally, because of their 'standard' nature, they also make excellent building blocks for services. Netowkr, process, filesystem, resource isolation are all presented in containres. The container has a network, IP address, and a bridge interface to talk to the local host including a veth pair.

## Images & Dockerfiles
You can think about images as the building or packing aspect of Docker and the containers as the running or execution aspect of Docker. The Dockerfile uses a basic DSL (Domain Specific Language) with instructions for building Docker images. We recommend the Dockerfile approach over docker commit because it provides a more repeatable, transparent, and idempotent mechanism for creating images. Each instruction adds a new layer to the image and then commits the image.

 Docker runs a container from the image. An instruction executes and makes a change to the container. Docker runs the equivalent of docker commit to commit a new layer. Docker then runs a new container from this new image. The next instruction in the file is executed, and the process repeats until all instructions have been executed.

[Stacked image]

As a result of each step being committed as an image, Docker is able to be really clever about building images. It will treat previous layers as a cache. If, in our debugging example, we did not need to change anything in Steps 1 to 3, then Docker would use the previously built images as a cache and a starting point. Essentially, it'd start the build process straight from Step 4. This can save you a lot of time when building images if a previous step has not changed. If, however, you did change something in Steps 1 to 3, then Docker would restart from the first changed instruction.

### Overlays
## Distributed microservices //Components
Machine lets you create Docker hosts on your computer, on cloud providers, and inside your own data center. It creates servers, installs Docker on them, then configures the Docker client to talk to them.

## Libnetwork
Docker was originally developed to improve the application development process. Docker allows developers to build an entire multi-tier application on a single Linux workstation without the complexity or overhead of multiple operating system images, as is the case with traditional virtualization. To accommodate the network requirements of this type of environment, Docker leverages simple network architecture.

As of version 1.9 of Docker, libnetwork is included in the main release of the project. This innovation was kickstarted when Docker acquired the SocketPlane team in March 2015. SocketPlane was one of the many available Software-Defined Networking solutions for containers on the market. Instead of connecting to a virtual bridge, each container would connect to an Open vSwitch (OVS) port. Container hosts with OVS running can form a virtual network overlay that would carry traffic destined for any container connected to the network. Containers seamlessly communicate with each other wherever they are – thus enabling true distributed applications. LibNetwork treats Network object at an abstract level to provide connectivity between a group of end-points that belong to the same network and isolate from the rest.

Docker’s networking code has now been included in a separate library called “libnetwork”. The idea of libnetwork is to codify the networking requirements for containers into a model, and provide an API and command-line tool based on that model. The premise of the libnetwork model is that containers can be joined to networks; the containers on a network can all communicate over that network. Modularity is an important factor. Speeding up DevOPS, bringing up connected containers becomes easy and combining components into microservices becomes much easier.

Libnetwork implements the Container Network Model (CNM) which relies on three main components. The sandbox, endpoints and networks. A Sandbox contains the configuration of a container's network stack. A Sandbox can have multiple endpoints attached to different networks. This includes management of the container's interfaces, routing table and DNS settings. A Sandbox may contain many endpoints from multiple networks. An Endpoint joins a Sandbox to a Network. An implementation of an Endpoint could be a veth pair, an Open vSwitch internal port or similar. An Endpoint can belong to only one network but may only belong to one Sandbox. A Network is a group of Endpoints that are able to communicate with each-other directly. An implementation of a Network could be a Linux bridge, a VLAN, etc. Networks consist of many endpoints. The goal of libnetwork is to deliver a robust Container Network Model that provides a consistent programming interface and the required network abstractions for applications. CNM is a generic model that does not only apply to Docker but can also be implemented in more traditional container projects like OpenVZ and LXC. The libnetwork APIs function as a common API for the plugins. 

By employing a model, libnetwork functions as a common ground for other overlay solutions. There are many networking solutions available to suit a broad range of use-cases. libnetwork uses a driver / plugin model to support all of these solutions while abstracting the complexity of the driver implementations by exposing a simple and consistent Network Model to users.

The network is managed by the CNM NetworkController object which exposes an API into libnetwork which allows (for example) Docker Engine to allocate and manage Networks. In essence NetworkController allows user to bind a particular driver to a given network. The Endpoint object provides the connectivity for services exposed by a container in a network with other services provided by other containers in the network.

The driver is the most abstract component of libnetwork and is not an user visible object. Drivers provide the actual implementation that makes the network work. The NetworkController however provides an API to configure the driver with specific options. Drivers can be both inbuilt (such as Bridge, Host, None & overlay) and remote (from plugin providers) to satisfy various usecases & deployment scenarios. Drivers registers with NetworkController. Build-in drivers registers inside of LibNetwork, while remote Drivers registers with LibNetwork via Plugin mechanism. (plugin-mechanism is WIP). Each driver handles a particular networkType.

The most commonly used driver is the 'bridge' driver. The bridge driver is an implementation that uses Linux Bridging and iptables to provide connectivity for containers It creates a single bridge, called docker0 by default, and attaches a veth pair between the bridge and every endpoint. This driver is discussed in detail in [LINK]. The overlay driver implements networking that can span multiple hosts using overlay network encapsulations such as VXLAN. 

## Key-Value stores
Multi-host networking uses a pluggable Key-Value store backend to distribute states using libkv. libkv supports multiple pluggable backends such as consul, etcd & zookeeper (more to come).




The Weave plugin runs automatically when you weave launch, provided your Docker daemon is version 1.9 or newer.


As for libnetwork plugin for flannel, we may pursue this direction as well. CoreOS is committed to Docker being one of the container options on our system so flannel will continue to work with it. It might be via a plugin or the way it is currently done (via --bip argument to Docker daemon).









 

It is advisable to name each individual container. This makes inspecting the log output easier.

 docker create command which creates a container but does not run it.

 sudo docker stats

 We call it the Ubuntu operating system, but really it is not the full operating system. It's a very cut-down version with the bare runtime required to run the distribution.

 Each image is being listed by the tags applied to it, so, for example, 12.04, 12.10, quantal, or precise and so on. Each tag marks together a series of image layers that represent a specific image (e.g., the 12.04 tag collects together all the layers of the Ubuntu 12.04 image). This allows us to store more than one image inside a repository.

 There are two types of repositories: user repositories, which contain images contributed by Docker users, and top-level repositories, which are controlled by the people behind Docker.



You can expose ports at run time with the docker run command with the --expose option. You can also specify a Git repository as a source for the Dockerfile as we can see here:

repository/name:tag
jamtur01/static_web:v1




WEAVEMESH
WEAVE

Important to mention is that libnetwork requires a kernel version of at least 3.16 to function. 

Install kernel version 3.19 for multi-host networks:
sudo apt-get install linux-generic-lts-vivid
sudo reboot
In order to support overlay networks


docker-machine create --driver 'generic' --generic-ip-address 127.0.0.1 weave-1 --generic-ssh-key

Weaveworks is the company that develops Weave. To application containers, the network established by weave looks like a giant Ethernet switch to which all the containers are connected. Weave creates a virtual network that connects Docker containers deployed across multiple hosts and enables their automatic discovery. Weave can traverse firewalls and operate in partially connected networks. Traffic can be encrypted, allowing hosts to be connected across an untrusted network.

Calico includes a driver for libnetwork that implements the Docker Container Network Model and supports networking of Docker containers the Calico way.

Calico
------
Every container gets its own IP address (or multiple addresses). No NAT or port mapping is used. Both IPv4 and IPv6 are supported. By default, containers with endpoints connected to the same network can communicate freely among themselves, but are firewalled off from other networks.
    Security policy can be fine-tuned by defining rules that control which groups of containers can reach which other groups (or the outside world) on which ports. You can think of Calico as providing a fully distributed lightweight firewall sitting in front of all of your containers.
    All traffic between containers is routed at L3 via the Linux kernel’s native IP forwarding engine in each host. Calico uses BGP (Border Gateway Protocol) as its control plane to advertise routes to individual containers across the physical network fabric. BGP is the routing protocol that powers the Internet, so scalability is one of Calico’s strong points.
    Containers networked with Calico can communicate directly (and securely) over IP with other containers, physical appliances, virtual machines and the public Internet without the need for any kind of specialized gateway function in the network.
    The entire solution is open source, just like Docker itself, and available today.


http://www.projectcalico.org/calico-dataplane-performance/

The value that every Docker project brings is clean interfaces and simplified integrations.

Different pods on a Kubernetes cluster need an overlay network of some sort to exchange packets. Without an overlay network, a container in one pod cannot get a packet to a container in a another pod. One way to provide this overlay network is to use flanneld.

Like other Docker projects, Docker Swarm follows the “swap, plug, and play” principle. As initial development settles, an API will develop to enable pluggable backends. This means you can swap out the scheduling backend Docker Swarm uses out-of-the-box with a backend you prefer.

Kubernetes - Manage applications, not machines

https://www.netdev01.org/docs/Networking%20in%20Containers%20and%20Container%20Clusters.pdf

Describe components

Docker has issued the 1.9 release of its container platform, which includes a way for containers to discover and link to each other. It's a big step toward reorganizing applications as sets of micro-services, each service having its own container, its own address, and its own ability to be upgraded as needed. The micro-service can move and its address will move with it, re-establishing its presence in a new location through the discovery mechanism built into Release 1.9.

They could see that containers were very different from virtual machines," Johnston said. Virtual machines are managed like physical servers that happen to exist in software. They're stood up and run continuously for months. Containers, on the other hand, may be activated, used for a single task, and then sent away in a matter of a few minutes.

http://www.informationweek.com/cloud/infrastructure-as-a-service/docker-adds-multi-host-networking-for-containerized-apps/d/d-id/1323006

Containers start almost instantly, are lightweight and provide application portability. Containers share the same operating system kernel, run on the same machine, include the application and all of its dependencies.

Swarm knows how to find a suitable server or set of servers for a given workload such as finding a host with lots of free RAM for a memory-intensive application.


But docker0 is no ordinary interface. It is a virtual Ethernet bridge that automatically forwards packets between any other network interfaces that are attached to it. This lets containers communicate both with the host machine and with each other. Every time Docker creates a container, it creates a pair of “peer” interfaces that are like opposite ends of a pipe — a packet sent on one will be received on the other. It gives one of the peers to the container to become its eth0 interface and keeps the other peer, with a unique name like vethAQI2QT, out in the namespace of the host machine. By binding every veth* interface to the docker0 bridge, Docker creates a virtual subnet shared between the host machine and every Docker container.

https://docs.docker.com/v1.7/articles/networking/


docs.weave.works/weave/latest_release/how-it-works.html

Weave creates a network bridge on the host. Each container is connected to that bridge via a veth pair, the container side of which is given an IP address & netmask supplied either by the user or Weave’s IP address allocator. Also connected to the bridge is the weave router container. Weave routers learn which peer host a particular MAC address resides on. They combine this knowledge with topology information in order to make routing decisions and thus avoid forwarding every packet to every peer. Weave can route packets in partially connected networks with changing topology. Project Calico on the other hand utilises BGP for routing between containers and aims for extreme scalability. 

The topology information captures which peers are connected to which other peers. Weave peers communicate their knowledge of the topology (and changes to it) to others, so that all peers learn about the entire topology. This communication occurs over the TCP links between peers, using a) spanning-tree based broadcast mechanism, and b) a neighour gossip mechanism.

The propagation of topology changes to all peers is not instantaneous, so it is very possible for a node elsewhere in the network to have an out-of-date view. If the destination peer for a packet is still reachable, then out-of-date topology can result in it taking a less efficient route. If the out-of-date topology makes it look as if the destination peer is not reachable, then the packet is dropped. For most protocols (e.g. TCP), the transmission will be retried a short time later, by which time the topology should have updated.

http://blog.weave.works/2015/06/12/weave-fast-datapath/

Version 1.2 includs fast datapath
http://blog.weave.works/2015/11/13/weave-docker-networking-performance-fast-data-path/

Effect of crypto on performance between containers?

Flanneld
========
https://github.com/coreos/flannel/blob/master/packet-01.png

Measurement tools
-----------------
https://github.com/esnet/iperf
qperf
netperf


All other Docker networking plugins, including Docker’s own “Overlay” driver, require that you set up Docker with a cluster store – a central database like Consul or Zookeeper – before you can use them. As well as being harder to set up, maintain and manage, every Docker host must be in constant contact with the cluster store: if you lose the connection, even temporarily, then you cannot start or stop any containers.

All cross-host coordination is handled by Weave Net’s “mesh” communication, using gossip and eventual consistency to avoid the need for constant communication and dependency on a central cluster store.

Weave
-----
To application containers, the network established by weave looks like a giant Ethernet switch to which all the containers are connected.

The Weave Net plugin actually provides two network drivers to Docker - one named weavemesh that can operate without a cluster store (like Docker’s overlay driver) and one named weave that can only work with one.

Weave creates a virtual network that connects Docker containers deployed across multiple hosts and enables their automatic discovery. Weave works alongside Docker's existing (single host) networking capabilities, so these can continue to be used by containers.

In any case where Weave can’t use fast data path between two hosts it will fall back to the slower packet forwarding approach used in prior releases. The selection of which forwarding approach to use is automatic, and made on a connection-by-connection basis. So a Weave network spanning two data centers might use fast data path within the data centers, but not for the more constrained network link between them.

	Explanation of Fast datapath
	http://blog.weave.works/2015/11/13/weave-docker-networking-performance-fast-data-path/

Weave operates at L2, as described at https://github.com/zettio/weave#how-does-it-work. It acquires knowledge of which MAC addresses are located at what peer hosts by looking at the Ethernet headers of captured packets, and at the weave encapsulation of packets it receives from other peers. Specifically, the concern is that because it uses pcap to implement an overlay network between containers in userspace it will introduce additional network latency, constrain network throughput, and take up CPU cycles that would otherwise be available to applications. And it routes packets based on the same sources of information. Main concern = performance of this approach and the number of context switches for per packet handling. Operations on the network require a quorate KV store. If quorum is not reached, these operations will simply fail. In practice this means that users may, for example, be unable to launch containers during a transient network partition.

Weave doesn't use an external consensus-based KV store as Weave’s back end, and instead went with a CRDT (Conflict-free Replicated Data Type) approach. Weave uses eventual consistency to manage network configuration. 

CONSISTENCY IN WEAVE EXPLAINED: https://www.youtube.com/watch?v=117gWVShcGU

Essentialy this means you have to install an additional distributed system in order to set up networking, for each Docker cluster, may not be to everyone’s taste. Scalability issues come into play when the amount of hosts in the KV store is extended beyond 5 to 10 hosts. Root cause analysis is harder: Figuring out whether bugs are in the application, or in Docker networking, or the external KV store, is up to you.

Weave is able to tunnel through firewalls, works with NAT, multicast, and reduced MTUs.  Weave  generally overcomes obstacles that, with other products, would require extensive manual intervention. It also comes with built-in encryption and supports cross-site deployments without special configuration.  This means you can basically trust it to run anywhere and with any topology.  By contrast Docker requires a full mesh of VXLAN tunnels between hosts, open ports for the KV store, and so on.

If you use Docker’s built-in networking, you must take responsibility for the installation and maintenance of an external key-value store.

	Using the built-in netwok drviers in Docker 1.9 requires that a consistent KV store is visible from all Docker hosts. In practice however this either means a) having the KV cluster in one of the datacentres, introducing a SPOF or b) spreading the KV cluster across multiple datacentres, greatly increasing the likelihood of transient partitions and hence quorum failure (with results as above)

Encryption of the connection between the containers is not a guarantee in standard Docker implementations. Overlay solutions allow you to do encryption [IS THIS TRUE FOR THE OVERLAY DRIVER?]

The Weave plugin gives you a closer integration with Docker. Weave implements service discovery for free, by providing a fast “micro DNS” server at each node. You simply name containers and everything ‘just works’, including load balancing across multiple containers with the same name. Weave implements service discovery for free, by providing a fast “micro DNS” server at each node. You simply name containers and everything ‘just works’, including load balancing across multiple containers with the same name.

We are aiming to make the use of fast datapath unobtrusive to Weave users. There are high-performance Software Defined Networking technologies out there, but unless you specialise in network administration, you might not find them very approachable.

Weave uses Open vSwitch Datapath, contributed to the Linux kernel by Open vSwitch. ODP by itself is not a full virtual network switch, but provides the packet-processing engine needed to implement one. ODP is commonly used in conjunction with the rest of the Open vSwitch suite to provide a full SDN solution, but it’s part of the kernel and you don’t need to install the rest of Open vSwitch to get it.

For Weave fast datapath, we have developed a Go library to control ODP, and modified the Weave Net router to delegate packet processing to ODP. The needs of the weave router don’t require most of the features and standards implemented by the rest of the Open vSwitch suite. Using ODP on its own allows us to take advantage of a proven technology, while keeping Weave just as easy to get started with as it always has been.

Weave has used a custom encapsulation format to wrap the packets from containers into UDP packets that are forwarded between hosts. Because fast datapath uses ODP, we are limited to use the standard encapsulation formats it supports. We have opted for vxlan, because it is supported by most kernel versions that have ODP, and it is based on UDP, so should work in any network environment where Weave already works. The required ODP and VXLAN features are present in Linux kernel versions starting with 3.12, and if your kernel was built without the necessary modules Weave Net falls back the “user mode” packet path.

We are aiming to have fast datapath work in a wide range of environments. But for those where it doesn’t, we plan to fall back to the existing Weave pcap-based datapath.
Fast data path reduces CPU overhead and latency because there are fewer copies of packet data and context switches. The packet goes straight from the user’s application to the kernel, which takes care of adding the VXLAN header

Another feature of Weave Net not supported by fast datapath is encryption. In legacy versions Weave used a shared key between all peers to do encryption. This is accomplished using the NaCl crypto libraries, employing Curve25519, XSalsa20 and Poly1305 to encrypt and authenticate messages. Peers that were started with a password do not continue with connection establishment unless they receive a public key from the remote peer. Thus either all peers in a weave network must be supplied with a password, or none.

Weave works by exposing the service and using iptables to NAT to the exposed container. A network of containers across more than two hosts can be established even when there is only partial connectivity between the hosts. Weave is able to route traffic between containers as long as there is at least one path of connected hosts between them.

So, for example, if a docker host in a local data centre can connect to hosts in GCE and EC2, but the latter two cannot connect to each other, containers in the latter two can still communicate; weave will route the traffic via the local data centre. In some situations all existing weave hosts may be unreachable from the new host due to firewalls, etc. However, it is still possible to add the new host, provided inverse connections, i.e. from existing hosts to the new hosts, are possible.

Commercial SDN solutions are available but Weave attempts to provide a simple way to connect containers. Weave peers continually exchange topology information, and monitor and (re)establish network connections to other peers. So if hosts or networks fail, weave can “route around” the problem.

weave connect/launch = equal
weave status connections
	fastp = fast datpath
	sleeve = legacy mode


The weave plugin container registers itself as a network driver when loaded, and will create a weave network and allocate IP addresses for containers when asked by libnetwork.

Bernstein’s NaCl library.

http://blog.weave.works/2015/06/12/weave-fast-datapath/
http://blog.weave.works/2015/06/16/weave-net-cryptography-faq/
https://github.com/weaveworks/weave/issues/36#issuecomment-57206811

##################
Enhances networking
##################
http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/enhanced-networking.html

Intro
-----
Containers can be moved between hosts without requiring any reconfiguration or, in many cases, restarts of other containers. All that is required is for the migrated container to be started with the same IP address as it was given originally.

Docker announced their acquisition of Socketplane, a start-up company working on software defined networking for Docker. This way the company tried to move away from the “all or nothing” monolith.  Customers do want to select implementations for services, and plug them into Docker. The APIs are not there yet to support this and they need to be.  It’s that simple.  We have all got to make this work. Courtesy of Socketplane.

Overlays allow for support for an “application centric” model in which any developer can create as many networks as they need – easily. 

Reasons for using Containers over Virtual Machines: https://github.com/ClusterHQ/docker-plugins

Service discovery with DNS can be done with SRV records. 

Extending Docker takes multiple forms: a plugin subsystem for Docker; network extensions as plugins; and volume extensions as plugins. Volume management is becoming modular aswell. Libnetwork provides the external driver API. 

Today Docker has released Docker 1.9, which includes advances in Docker Networking. Perhaps the most important is the introduction of a new overlay networking approach to connect docker containers running across multiple hosts, which means that “out of the box” Docker has multi-host networking.

This year we have seen Docker transition to wider production use, where networking is vital to support clustering, replication and so on. Up to now, customers have either hand coded/wired Docker networking or used a special product like Weave Net.

# NOTE: Since servers in GTS are initially deployed with the same hostname, a reboot of the
# etcd server may be required in order to update the key-value pairs. Afterwards, the etcd
# service on the master node has to be started (This script doesn't include an init script).
# Lastly, the second node has to export the ETCD_AUTHORITY environment variable again and run
# 'calicoctl node'. At this point a BGP relationship between the nodes should be established.

Docker’s networking code has been factored out into its own library called “libnetwork”. The idea of libnetwork is to codify the networking requirements for containers into a model, and provide an API and command-line tool based on that model.

Docker network modes: “bridge”, “host”, and so on. These are implemented in libnetwork as drivers, which provide an OS-level implementation of libnetwork’s model. For instance, the bridge driver creates a Linux bridge device for a network, and gives each container joined to the network an interface on that bridge. Tunneling with a Veth pair. Ref Joris.

Libnetwork includes a proxy which forwards driver operations to a remote process, called a remote driver. The Weave plugin acts as a remote driver. Because Docker (or rather, libnetwork) explicitly enrols the Weave plugin to drive networks, there is a closer integration between them. And, other tools like Docker Swarm and Docker Compose do not have to make concessions or workarounds for working with Weave. 

It also means the weave plugin gets a much more narrow view of what is going on (e.g., it doesn’t get told the container name), so it cannot offer the full range of weave features other than by workarounds. Depending on the openness of Docker this can be improved. 

Docker Networking in 1.9 requires an external Key-Value (KV) store, which is used for global IP address allocation and node discovery. The store is accessed via an API, libkv, that is advertised as working with Consul, etcd, and ZooKeeper.

Related work
------------
It should be noted that these performance measurments have been taken with the Enhanced Networking feature enabled. This requires that its kernel has the ixgbevf module installed and that you set the sriovNetSupport attribute for the instance.

The TCP bandwidth is rather disappointing! This is due to the MTU issue mentioned above. The network interfaces on the host are configured with an MTU of 9000 bytes, as is usual with 10Gb/s networks. We can override the MTU of the weave network by setting the environment variable WEAVE_MTU. Vxlan encapsulation has an overhead of 50 bytes, so we set WEAVE_MTU to 8950, and relaunch weave and the containers. Then repeating the qperf tests gives a more respectable result. there is some overhead due to weave fast datapath, but the results are close to those of host networking.

The original CNM model proposal:
https://github.com/docker/docker/issues/9983

Weave talks about a relevent note of caution, as many cloud comuting environments implement SDN in their cloud, VXLAN traffic may get a different treatment throughout the network which can cause strange effects. 

Another point to note is that native TCP network throughput is assisted by the TSO/LRO (TCP Segmentation Offload / Large Receive Offload) support of modern network interface chipsets. With these facilities, the network interface hardware takes on some of the burden of segmenting a TCP data stream into packets, and reassembling it on the receiver. This helps to avoid CPU being the bottleneck to network throughput even when using a traditional 1500 byte MTU. But conventional TSO/LRO does not support the further packet manipulations needed for VXLAN encapsulation (hardware VXLAN offload does exist, but currently only in high-end NICs). So, with VXLAN, more CPU work is required to sustain a given TCP throughput, and this CPU usage may present a bottleneck. Again, any use of VXLAN is subject to this effect. [DOES GTS USE VXLAN OFFLOADING IN THEIR NICS?]

The WEAVE_MTU environment variable when running weave launch sets the MTU for the weave network. There is a trade-off: Set the MTU too low and performance suffers. Set it too high, and the WEAVE_MTU plus the VXLAN tunnel overhead of 50 bytes causes the packets to exceed the MTU of the underlying network. In this situation Weave Net will fall back to its user space encapsulation. The default value of WEAVE_MTU is 1410, which is a conservative value that should work in almost all network environments. But if you know that the underlying network supports a higher MTU, you can set it to obtain improved performance. AWS EC2 supports 9000 byte jumbo frames for many instance types, so we can safely set WEAVE_MTU to 8950.

http://blog.weave.works/2015/11/13/weave-docker-networking-performance-fast-data-path/

------
Calico
------
Project Calico, which uses standard L3 networking for endpoints (VMs or containers) to try to get past some of the scalability issues with L2 (among other reasons). 


The problem of default Docker networking
----------------------------------------
By default, Docker uses host-private networking. It creates a virtual bridge, called docker0 by default, and allocates a subnet from one of the private address blocks defined in RFC1918 for that bridge. For each container that Docker creates, it allocates a virtual ethernet device (called veth) which is attached to the bridge. The veth is mapped to appear as eth0 in the container, using Linux namespaces. The result is that Docker containers can talk to other containers only if they are on the same machine (and thus the same virtual bridge). Difficulty ensues when containers on different machines try to reach each other. In order for Docker containers to communicate across nodes, they must be allocated ports on the machine’s own IP address, which are then forwarded or proxied to the containers. This obviously means that containers must either coordinate which ports they use very carefully or else be allocated ports dynamically. 

Benefits of using an overlay
----------------------------
Connecting the containers via an overlay solution means that all containers can communicate with other containers via the container IP address and port inside the Weave network. All [NODES] can communicate with containers via the container IP address and port inside the Weave network. Containers do not have to be statically linked to each other to be able to communicate. Forwarding / co-ordinating ports from the host machine is not required
 

Virtual machines in GTS are connected to the NIC of the pod by pci_passthrough

QPERF
https://launchpadlibrarian.net/82234527/qperf_0.4.6-0.1.gb81434e-OFED-1.5.2-1ubuntu1_amd64.deb
qperf -t 10 -ub 172.16.0.x udp_bw udp_lat



“Networking is a critical part of the stack for distributed applications and has become an increasing area of focus within the Docker partner ecosystem due to the rapid growth in multi-container, multi-host applications,” said Solomon Hykes, chief architect of the Docker Project and founder and CTO of Docker, Inc.

Weave automatically chooses the fastest available method to transport data between peers. The most performant of these ('fastdp’) offers near-native throughput and latency but does not support encryption; consequently supplying a password will cause the router to fall back to a slower mode ('sleeve’) that does, for connections that traverse untrusted networks

Weave includes a Docker API proxy so that containers launched via the Docker command-line interface or remote API are attached to the weave network before they begin execution.

Weave supports load balancing based on their WeaveDNS service discovery. Containers with the same name are member of the loadbalancing group. 

Weave implements an overlay network between Docker hosts, so each packet is encapsulated in a tunnel header and sent to the destination host, where the header is removed. In previous releases, the Weave router added/removed the tunnel header.









CALICO
==============================
Calico is a networking method for interconnecting virtual ‘workloads’ together.  I’m deliberately using the word ‘workloads’ here instead of Virtual Machines/Containers/etc. because Calico could apply to any or all of them.




Learn | Project Calico
http://www.projectcalico.org/learn/

Announcing Calico 1.2! | Project Calico
http://www.projectcalico.org/announcing-calico-1-2/

Docker 1.9 includes network plugin support and Calico is ready! | Project Calico
http://www.projectcalico.org/docker-libnetwork-is-almost-here-and-calico-is-ready/

OpenStack Liberty – now with added Calico | Project Calico
http://www.projectcalico.org/openstack-liberty-now-with-added-calico/

Calico dataplane performance | Project Calico
http://www.projectcalico.org/calico-dataplane-performance/

Calico and containers are flip sides of the same coin | Project Calico
http://www.projectcalico.org/calico-and-containers-are-flip-sides-of-the-same-coin/

Using etcd for elections | Project Calico
http://www.projectcalico.org/using-etcd-for-elections/

Moving Calico to a distributed data store using etcd | Project Calico
http://www.projectcalico.org/moving-calico-to-a-distributed-data-store-using-etcd/

Using Ethernet as the interconnect fabric for a Calico installation | Project Calico
http://www.projectcalico.org/using-ethernet-as-the-interconnect-fabric-for-a-calico-installation/

Why BGP? | Project Calico
http://www.projectcalico.org/why-bgp/

Why Calico? | Project Calico
http://www.projectcalico.org/why-calico/

Tab-Snap - Chrome Web Store
https://chrome.google.com/webstore/detail/tab-snap/ajjloplcjllkammemhenacfjcccockde/related


https://blog.midonet.org/docker-networking-midonet/

http://blog.ipspace.net/2015/06/project-calico-is-it-any-good.html
