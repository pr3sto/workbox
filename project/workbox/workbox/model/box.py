# -*- coding: utf-8 -*-
"""
Virtual working environment (box) related model.

"""

from ming import schema as s
from ming.odm import FieldProperty, ForeignIdProperty, RelationProperty
from ming.odm.declarative import MappedClass

from workbox.model import DBSession
from workbox.model import User

__all__ = ['Box']


class Box(MappedClass):
    """
    Box definition.

    """
    class __mongometa__:
        session = DBSession
        name = 'boxes'

    _id = FieldProperty(s.ObjectId)
    box_id = FieldProperty(s.Int)

    datetime_of_creation = FieldProperty(s.datetime)
    datetime_of_modify = FieldProperty(s.datetime)

    _user = ForeignIdProperty(User)
    user = RelationProperty(User)

    status = FieldProperty(s.String)
    name = FieldProperty(s.String)
    vagrantfile_path = FieldProperty(s.String)
