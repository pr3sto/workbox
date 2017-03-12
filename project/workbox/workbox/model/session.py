# -*- coding: utf-8 -*-
"""Session model"""

from ming import Session
from ming.odm import ThreadLocalODMSession

mainsession = Session()
DBSession = ThreadLocalODMSession(mainsession)
