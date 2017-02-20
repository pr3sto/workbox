#!/bin/bash

# create debian configurations
pip install make-deb
make-deb

# install dependencies
apt-get -y install debhelper dh-virtualenv

# build package
dpkg-buildpackage -us -uc
