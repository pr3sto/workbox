#!/bin/bash

apt-get update

# apache
apt-get -y install apache2 libapache2-mod-wsgi 

# mongodb
apt-get -y install mongodb

# vagrant
apt-get -y install vagrant

# docker
apt-get -y install docker.io
ln -sf /usr/bin/docker.io /usr/local/bin/docker
sed -i '$acomplete -F _docker docker' /etc/bash_completion.d/docker.io

# autostart at boot
update-rc.d apache2 defaults
update-rc.d docker.io defaults
update-rc.d mongod defaults
