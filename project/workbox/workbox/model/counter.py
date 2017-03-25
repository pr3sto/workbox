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

    _id (string): name if collection of ids
    uid (int): autoincremented id

    """

    class __mongometa__:
        session = DBSession
        name = 'counter'

    _id = FieldProperty(s.String)
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
            query={'_id': name}, update={'$inc': {'uid': 1}}, new=True).uid
