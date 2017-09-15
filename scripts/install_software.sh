#!/bin/bash

/usr/bin/apt-get update

# apache
/usr/bin/apt-get -y install apache2 libapache2-mod-wsgi 

# vagrant
/usr/bin/apt-get -y install vagrant
