# -*- coding: utf-8 -*-
"""Setup the workbox application"""

from __future__ import print_function, unicode_literals
from workbox import model


def bootstrap(command, conf, vars):
    """Place any commands to setup workbox here"""

    # <websetup.bootstrap.before.auth>

    g = model.Group()
    g.group_name = 'managers'
    g.display_name = 'Managers Group'

    p = model.Permission()
    p.permission_name = 'manage'
    p.description = 'This permission gives an administrative right'
    p.groups = [g]

    u = model.User()
    u.user_name = 'admin'
    u.display_name = 'Administrator'
    u.groups = [g]
    u.password = 'admin'

    model.DBSession.flush()
    model.DBSession.clear()

    # <websetup.bootstrap.after.auth>
