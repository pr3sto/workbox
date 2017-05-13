APP_CONFIG = "/opt/venvs/workbox/lib/python2.7/site-packages/workbox/appconfig/configuration.ini"

#Setup logging
import logging.config
logging.config.fileConfig(APP_CONFIG)

#Load the application
from paste.deploy import loadapp
application = loadapp('config:%s' % APP_CONFIG)
