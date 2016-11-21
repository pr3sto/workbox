# -*- coding: utf-8 -*-
"""The application's model objects"""

import ming.odm
from .session import mainsession, DBSession


def init_model(engine):
    """Call me before using any of the tables or classes in the model."""
    mainsession.bind = engine
    ming.odm.Mapper.compile_all()

    for mapper in ming.odm.Mapper.all_mappers():
        mainsession.ensure_indexes(mapper.collection)

# Import your model modules here.
from hellomongo.model.auth import User, Group, Permission
from hellomongo.model.container import container

__all__ = ('User', 'Group', 'Permission')
