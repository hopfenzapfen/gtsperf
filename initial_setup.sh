#!/bin/bash
# Check for root priviliges
# Make sure only root can run our script
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

#Change the hostname
echo "Enter a hostname" && read "HOSTNAME"
hostname $HOSTNAME && echo $HOSTNAME>/etc/hostname
sed -i -e 's/sa2host/'$HOSTNAME'/' /etc/hosts

#Install Docker
read -r -p "Install Docker? [Y/n] " response
response=${response,,}    # tolower
if [[ $response =~ ^(yes|y)$ ]]; then
	sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
	sudo echo "deb https://apt.dockerproject.org/repo ubuntu-trusty main" > /etc/apt/sources.list.d/docker.list
	sudo apt-get -yqq update && sudo apt-get install -yqq docker-engine
fi
