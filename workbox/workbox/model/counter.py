# -*- coding: utf-8 -*-
"""Counter model"""

from ming import schema as s
from ming.odm import FieldProperty
from ming.odm.declarative import MappedClass

from workbox.model import DBSession

__all__ = ['Counter']


class Counter(MappedClass):
    """
    Counter definition

    """

    class __mongometa__:
        session = DBSession
        name = 'counter'

    _id = FieldProperty(s.ObjectId)
    name = FieldProperty(s.String)
    uid = FieldProperty(s.Int)

    @staticmethod
    def get_next_id(name):
        """
        Get next id to specified name

        Args:
            name (string): name of id collection

        Returns:
            Next autoincremented id

        """

        return Counter.query.find_and_modify(
            query={'name': name}, update={'$inc': {'uid': 1}}, new=True).uid
