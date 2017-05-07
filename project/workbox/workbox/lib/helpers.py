# -*- coding: utf-8 -*-
"""Template Helpers used in workbox"""

import logging
from datetime import datetime
from markupsafe import Markup
import psutil

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
    

try:
    from webhelpers2 import date, html, number, misc, text
except SyntaxError:
    log.error("WebHelpers2 helpers not available with this Python Version")
