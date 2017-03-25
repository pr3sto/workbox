# -*- coding: utf-8 -*-
"""Setup the workbox application"""

from __future__ import print_function, unicode_literals
from workbox import model


def bootstrap(command, conf, vars):
    """First setup of workbox"""

    # <websetup.bootstrap.before.auth>

    gm = model.Group()
    gm.group_name = 'managers'
    gm.display_name = 'Managers Group'

    gu = model.Group()
    gu.group_name = 'users'
    gu.display_name = 'Users Group'

    pm = model.Permission()
    pm.permission_name = 'manage'
    pm.description = 'This permission gives an administrative right'
    pm.groups = [gm]

    pu = model.Permission()
    pu.permission_name = 'use'
    pu.description = 'This permission gives basic rights'
    pu.groups = [gu]

    u = model.User()
    u.user_name = 'admin'
    u.display_name = 'Administrator'
    u.groups = [gm]
    u.password = 'admin'

    box_counter = model.Counter()
    box_counter._id = 'box'
    box_counter.uid = 0

    history_counter = model.Counter()
    history_counter._id = 'history'
    history_counter.uid = 0

    model.DBSession.flush()
    model.DBSession.clear()

    # <websetup.bootstrap.after.auth>
