#!/bin/bash

set -e

# install dependencies
apt-get update
apt-get -y install python python-dev python-virtualenv
apt-get -y install debhelper dh-virtualenv

# create venv for project
cd ../
virtualenv --no-site-packages workboxenv

# copy project to venv directory
cp -r workbox workboxenv/workbox

# activate venv
cd workboxenv/
. bin/activate

# install turbogears dependencies
pip install tg.devtools
# deb package maker dependencies
pip install make-deb

# create debian configurations
cd workbox/
make-deb

# copy all scripts
cp ../../scripts/preinst ./debian
cp ../../scripts/postinst ./debian
cp ../../scripts/prerm ./debian
cp ../../scripts/postrm ./debian

# add service dependencies
awk -i inplace '/Depends:/{print $0 ", apache2, libapache2-mod-wsgi (>= 4.3), mongodb-org (>= 3.0), vagrant (>= 1.9)"; next}1' ./debian/control

# build package
dpkg-buildpackage -us -uc
cp ../workbox_*.deb ../../

# cleanup
rm -f preinst
rm -f postinst
rm -f prerm
rm -f postrm
rm -f make_deb_package.sh
rm -rf debian/
rm -f ../${PWD##*/}_*
rm -f ../${PWD##*/}-*

# deactivate venv
deactivate

# exit
GREEN='\033[0;32m'
printf "\n${GREEN}Done\n\n"
