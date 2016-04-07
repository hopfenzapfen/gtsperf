#!/bin/bash

# This script provides a quick method to bootstrap a host into an overlay node.
# The script is meant to be executed on a newly deployed (virtual) machine. It
# will install Docker and provide an option to kickstart the installation of
# either Weave, Calico or Flannel. If required, the follow-up script provides
# a choice to configure the VM as either a master or a slave node.

# Check for root priviliges
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

# Change the hostname
echo "Enter a hostname" && read "HOSTNAME"
hostname $HOSTNAME && echo $HOSTNAME>/etc/hostname
sed -i -e 's/sa2host/'$HOSTNAME'/' /etc/hosts

# Install Docker
read -r -p "Install Docker? [y/n] " RESPONSE
RESPONSE=${RESPONSE,,}
if [[ $RESPONSE =~ ^(yes|y)$ ]]; then
  source /etc/lsb-release
	sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
	sudo echo "deb https://apt.dockerproject.org/repo ubuntu-$DISTRIB_CODENAME main" > /etc/apt/sources.list.d/docker.list
  printf "\nUpdating sources and installing Docker. Please wait..."
  sudo apt-get -yqq update && sudo apt-get install -yqq docker-engine
  # Ensure that Docker is running
  SERVICE=docker
  if (( $(ps -ef | grep -v grep | grep $SERVICE | wc -l) > 0 )); then
    echo "The $SERVICE service is running."
  else
    service $SERVICE start
  fi
else
  echo "WARNING: by not choosing to install Docker, installing an overlay solution may fail."
  read -r -p "Are you sure you want to continue? [y/n] " RESPONSE
  response=${RESPONSE,,}
  if [[ $RESPONSE =~ ^(no|n)$ ]]; then
    exit 1
  fi
fi

# Increase kernel version to 3.19
echo "Upgrading kernel version..."
sudo apt-get install -yqq linux-generic-lts-vivid

# Overlay selection
printf "\nOptions\n-------\n1. Weave\n2. Calico\n3. Flannel\n4. None\nSelect an overlay: "
read INPUT
case $INPUT in
    1 ) printf "\nYou selected 'Weave'."
		printf " Press ENTER to bootstrap overlay."; read; cd ./Overlays/Weave/; ./setup.sh;;
    2 ) printf "\nYou selected 'Calico'."
		printf " Press ENTER to bootstrap overlay."; read; cd ./Overlays/Calico/; ./setup.sh;;
    3 ) printf "\nYou selected 'Flannel'."
		printf " Press ENTER to bootstrap overlay."; read; cd ./Overlays/Flannel/; ./setup.sh;;
    *)  printf "You selected not to install an overlay solution."; break;;
esac
