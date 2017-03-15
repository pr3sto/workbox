# -*- coding: utf-8 -*-
"""
Autoincrement id model.

"""

from ming import schema as s
from ming.odm import FieldProperty
from ming.odm.declarative import MappedClass

from workbox.model import DBSession

__all__ = ['AutoincId']


class AutoincId(MappedClass):
    """
    Autoincrement id definition.

    _id: name if collection of ids;
    uid: autoincrement id.

    """
    class __mongometa__:
        session = DBSession
        name = 'autoincids'

    _id = FieldProperty(s.String)
    uid = FieldProperty(s.Int)

    @staticmethod
    def get_next_id(name):
        return AutoincId.query.find_and_modify(
            query={'_id': name}, update={'$inc': {'uid': 1}}, new=True
        ).uid
