# -*- coding: utf-8 -*-
"""The application's model objects"""

import ming.odm
from .session import mainsession, DBSession


def init_model(engine):
    """Call me before using any of the tables or classes in the model"""

    mainsession.bind = engine
    ming.odm.Mapper.compile_all()

    for mapper in ming.odm.Mapper.all_mappers():
        mainsession.ensure_indexes(mapper.collection)


from workbox.model.auth import User, Group, Permission
from workbox.model.counter import Counter
from workbox.model.box import Box
from workbox.model.vagrantfile_template import VagrantfileTemplate
from workbox.model.history import History 


__all__ = ['User', 'Group', 'Permission', 'Counter', 'Box', 'VagrantfileTemplate', 'History']
