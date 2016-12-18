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
    u.user_name = 'manager'
    u.display_name = 'Mr Manager'
    u.groups = [g]
    u.password = 'managerpass'

    u1 = model.User()
    u1.user_name = 'teacher'
    u1.display_name = 'Mr Teacher'
    u1.password = 'teacherpass'

    model.DBSession.flush()
    model.DBSession.clear()

    # <websetup.bootstrap.after.auth>
