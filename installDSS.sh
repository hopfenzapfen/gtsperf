#!/bin/bash

SERVERDIR=DarwinStreamingSrvr6.0.3-Source
PATCH1=dss-6.0.3.patch
PATCH2=dss-hh-20080728-1.patch

# make sure its run as sudo
# Check for root priviliges
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

# download and unpack the server source
echo "Downloading server source files ..."
wget http://dss.macosforge.org/downloads/DarwinStreamingSrvr6.0.3-Source.tar
tar xf DarwinStreamingSrvr6.0.3-Source.tar

# download patches
echo "Downloading patches ..."
wget http://parsa.epfl.ch/cloudsuite/software/darwin/dss-6.0.3.patch
wget http://parsa.epfl.ch/cloudsuite/software/darwin/dss-hh-20080728-1.patch
wget http://parsa.epfl.ch/cloudsuite/software/darwin/Install
chmod +x Install

# create user
echo "Creating qtss user and group ..."
sudo addgroup qtss
sudo adduser --system --no-create-home --ingroup qtss qtss

echo "Installing dependencies ..."
sudo apt-get install -yq libstdc++5
sudo apt-get install -yq build-essential
sudo apt-get remove -yq gcc gcc-4.8
sudo apt-get install -yq g++

# install correct compiler version
echo "Installing gcc 4.4 (this can take a while) ..."
sudo apt-get install -yq gcc-4.4
sudo cp /usr/bin/gcc-4.4 /usr/bin/gcc

echo "Installing g++ 4.4 (this can take a while) ..."
sudo apt-get install -yq g++-4.4
sudo cp /usr/bin/g++-4.4 /usr/bin/g++

# move patches
mv $PATCH1 $SERVERDIR 
mv $PATCH2 $SERVERDIR
mv Install $SERVERDIR

# apply patches
cd $SERVERDIR
patch -p1 < $PATCH1
patch -p1 < $PATCH2


# install server
./Builtit
./Install

