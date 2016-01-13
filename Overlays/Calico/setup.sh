#!/bin/bash

# Installing Calico with etcd from project PPA's.
# Please update the OpenStack version if you run this script in the future.
echo "Installing Calico. Please wait..."
apt-add-repository ppa:project-calico/kilo
add-apt-repository ppa:cz.nic-labs/bird
apt-get update && apt-get install etcd python-etcd

# Configure etcd
cd /etc/init/
ETCDIP=/sbin/ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'
echo 'exec /usr/bin/etcd --name="node1" \' >> etcd.conf
echo "--advertise-client-urls=\"http://$ETCDIP:2379,http://$ETCDIP:4001\" \\" >> etcd.conf
echo '--listen-client-urls="http://0.0.0.0:2379,http://0.0.0.0:4001" \' >> etcd.conf
echo '--listen-peer-urls "http://0.0.0.0:2380" \' >> etcd.conf
echo "--initial-advertise-peer-urls \"http://$ETCDIP:2380\" \\" >> etcd.conf
echo '--initial-cluster-token $(uuidgen) \' >> etcd.conf
echo "--initial-cluster \"node1=http://$ETCDIP:2380\" \\" >> etcd.conf
echo '--initial-cluster-state "new"' >> etcd.conf
cd ~/ && service etcd startca

# Install the Calico component
wget https://github.com/projectcalico/calico-docker/releases/download/v0.13.0/calicoctl
chmod +x calicoctl
mv calicoctl /usr/bin/


# Starting the Weave component
read -r -p "Is this the first Calico node in the network? [y/n] " RESPONSE
RESPONSE=${RESPONSE,,}
if [[ $RESPONSE =~ ^(yes|y)$ ]]; then
  calicoctl node
else
  read -r -p "Enter the IP address of the etcd node in the network: " MASTER_IP
  # Refer to the etcd authority, previously set up  
  export ETCD_AUTHORITY=$MASTER_IP:2379
  calicoctl node
fi



