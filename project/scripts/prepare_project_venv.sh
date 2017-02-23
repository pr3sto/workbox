#!/bin/bash

if [ "$#" -ne 1 ] 
then
	echo "Usage: $0 project_name. Please specify project name."
	exit
fi

# install venv
/usr/bin/apt-get update
/usr/bin/apt-get -y install python python-virtualenv

# create and activate venv for project
/usr/local/bin/virtualenv --no-site-packages $1env
cd $1env

# turbogears dependencies
source bin/activate
bin/pip install tg.devtools
deactivate

# create folder for project
/bin/mkdir work
