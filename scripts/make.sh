#!/bin/bash

cd ../

# install venv
apt-get update
apt-get -y install python python-virtualenv

# create venv for project
virtualenv --no-site-packages workboxenv

# copy project to venv directory
cp -r workbox workboxenv/workbox

# copy all scripts
cp scripts/preinst workboxenv/workbox/preinst
cp scripts/postinst workboxenv/workbox/postinst
cp scripts/prerm workboxenv/orkbox/prerm
cp scripts/postrm workboxenv/workbox/postrm
cp scripts/make_deb_package.sh workboxenv/workbox/make_deb_package.sh

# navigate to venv
cd workboxenv/

# activate venv
. bin/activate

# install turbogears dependencies
pip install tg.devtools

# build deb
cd workbox/
./make_deb_package.sh

# copy deb package
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
clear
GREEN='\033[0;32m'
printf "\n${GREEN}Done\n\n"
