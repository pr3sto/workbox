#!/bin/bash

# create debian configurations
pip install make-deb
make-deb

# add scripts
cp preinst ./debian
cp postinst ./debian
cp prerm ./debian
cp postrm ./debian

# add service dependencies
awk -i inplace '/Depends:/{print $0 ", apache2, libapache2-mod-wsgi (>= 4.3), mongodb-org (>= 3.0), vagrant (>= 1.9)"; next}1' ./debian/control

# install buildpackage dependencies
apt-get update
apt-get -y install debhelper dh-virtualenv

# build package
dpkg-buildpackage -us -uc
