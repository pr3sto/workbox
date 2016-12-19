# -*- coding: utf-8 -*-
"""Setup the Project application"""

from __future__ import print_function, unicode_literals
from project import model


def bootstrap(command, conf, vars):
    """Place any commands to setup project here"""

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
    u.display_name = 'Admin'
    u.groups = [g]
    u.password = 'admin'

    model.DBSession.flush()
    model.DBSession.clear()

    # <websetup.bootstrap.after.auth>
