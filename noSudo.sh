#!/bin/sh

# add the "gts" user to docker group to allow running it without sudo (see: http://askubuntu.com/a/477554)
sudo gpasswd -a gts docker
newgrp docker
sudo service docker restart