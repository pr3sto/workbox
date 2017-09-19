#!/bin/sh

RED='\033[0;31m'
NC='\033[0m'

# service mongod should be started
if ps ax | grep -v grep | grep mongod > /dev/null
then

  # setup workbox
  . /opt/venvs/workbox/bin/activate
  cd /opt/venvs/workbox
  /opt/venvs/workbox/bin/gearbox setup-app -c /opt/venvs/workbox/lib/python2.7/site-packages/workbox/appconfig/configuration.ini
  deactivate

else

  printf "\n${RED}Error:${NC} service mongod not started\n\n"
  exit 1

fi

