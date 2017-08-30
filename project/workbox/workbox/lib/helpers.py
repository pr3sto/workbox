# -*- coding: utf-8 -*-
"""Template Helpers used in workbox"""

import logging
import socket
from datetime import datetime
from markupsafe import Markup
import psutil
import tg

log = logging.getLogger(__name__)


def current_year():
    """ Return current year. """

    now = datetime.now()
    return now.strftime('%Y')

def is_docker_enabled():
    """ Detect if docker service is started. """

    for proc in psutil.process_iter():
        if 'docker' in proc.name():
            return True
    return False

def get_server_load_value():
    """ Get server load value. """

    return psutil.virtual_memory().percent

def get_free_port():
    """ Find and returns free port number. """

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.bind(("", 0))
    free_port = soc.getsockname()[1]
    soc.close()
    return free_port

def get_vagrantfiles_base_folder():
    """ Return base folder for vagrantfiles. """

    return tg.config.get('workbox.vagrantfiles.basefolder')

def get_hostname():
    """ Return hostname. """

    return tg.config.get('workbox.hostname')

try:
    from webhelpers2 import date, html, number, misc, text
except SyntaxError:
    log.error("WebHelpers2 helpers not available with this Python Version")
