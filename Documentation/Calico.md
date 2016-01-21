Due to the way the virtual machines are provisioned in GTS, it is impossible to create a fully functional meshed topology as depicted in figure [FIGURE] with Calico. The BIRD routing daemon, which lies at the core of Calico, refuses to import a route from the kernel if the nexthop is not in a directly connected network. This essentially means that only physically connected networks can be included in the routing table as a correct BGP route, effectively limiting the topology to a star. A workaround in order to include the links that are not directly connected to the routing table would be to issue a route to said link and specify the route as 'onlink'. By issuing this next hop flag (NHFLAG) with the \texttt{ip} command, the networking stack will pretend that the nexthop is directly attached to the given link, even if it does not match any interface prefix. The NHFLAG parameter essentially instructs the kernel to treat the route as a connected network. 

However, specifying this flag in the GTS returns that the NHFLAG is an invalid argument for the specified virtual interface. This means that Calico's overlay solution is limited to point-to-point topologies between sites in GTS.



[SOURCE] http://marc.info/?l=bird-users&m=139809577125938&w=2
