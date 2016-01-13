#!/bin/bash
# Installing Weave Net
echo "Installing Weave Net. Please wait..."
sudo curl -L git.io/weave -o /usr/local/bin/weave
sudo chmod +x /usr/local/bin/weave

# Starting the Weave component
read -r -p "Is this the first Weave node in the network? [y/n] " RESPONSE
RESPONSE=${RESPONSE,,}
if [[ $RESPONSE =~ ^(yes|y)$ ]]; then
  weave launch &&  weave status
else
  read -r -p "Enter the IP address of an existing Weave router in the network: " ROUTER_IP
  weave launch $ROUTER_IP && weave status
fi
