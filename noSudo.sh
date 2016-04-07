#!/bin/sh

# add user to docker group to allow running it without sudo (see: http://askubuntu.com/a/477554)
sudo gpasswd -a ${USER} docker
sudo service docker restart
newgrp docker