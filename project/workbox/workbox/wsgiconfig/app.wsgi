APP_CONFIG = "/opt/venvs/workbox/lib/python2.7/site-packages/workbox/wsgiconfig/production.ini"

#Setup logging
import logging.config
logging.config.fileConfig(APP_CONFIG)

#Load the application
from paste.deploy import loadapp
application = loadapp('config:%s' % APP_CONFIG)
