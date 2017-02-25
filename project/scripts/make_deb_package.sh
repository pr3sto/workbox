#!/bin/bash

# create debian configurations
/usr/bin/pip install make-deb
/usr/local/bin/make-deb

# add scripts
/bin/cp preinst ./debian
/bin/cp postinst ./debian
/bin/cp prerm ./debian
/bin/cp postrm ./debian

# add service dependencies
/usr/bin/awk -i inplace '/Depends:/{print $0 ", apache2, libapache2-mod-wsgi (>= 4.3), mongodb-org (>= 3.0), vagrant (>= 1.8), docker (>= 1.5)"; next}1' ./debian/control

# install buildpackage dependencies
/usr/bin/apt-get update
/usr/bin/apt-get -y install debhelper dh-virtualenv

# build package
/usr/bin/dpkg-buildpackage -us -uc
