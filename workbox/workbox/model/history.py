# -*- coding: utf-8 -*-
"""History records related model"""

from datetime import datetime

from ming import schema as s
from ming.odm import FieldProperty, ForeignIdProperty, RelationProperty
from ming.odm.declarative import MappedClass

from workbox.model import DBSession
from workbox.model import User, Box, Counter

__all__ = ['History']


class History(MappedClass):
    """
    History record defenition

    """

    class __mongometa__:
        session = DBSession
        name = 'history'

    _id = FieldProperty(s.ObjectId)
    history_id = FieldProperty(s.Int)

    _user_id = ForeignIdProperty(User)
    user = RelationProperty(User)

    _box_id = ForeignIdProperty(Box)
    box = RelationProperty(Box)

    datetime = FieldProperty(s.datetime)

    info = FieldProperty(s.String)

    @staticmethod
    def add_record(user_name, box_id, info):
        """
        Add new history record to db

        Args:
            user_name (string): user name
            box_id (id): related box id in db
            info (string): info

        """

        record = History()
        record.history_id = Counter.get_next_id('history')
        record.user = User.query.get(user_name=user_name)
        if box_id is not None:
            record.box = Box.query.get(box_id=box_id)
        record.datetime = datetime.now()
        record.info = info

        DBSession.flush()
        DBSession.clear()

    @staticmethod
    def get_all_user_records(user_id):
        """
        Get all user history records from db

        Args:
            user_id (int): user id in db

        Returns:
            Collection of all history records

        """

        return History.query.find({'_user_id': user_id})

    @staticmethod
    def get_all_records():
        """
        Get all history records from db

        Returns:
            Collection of all history records

        """

        return History.query.find()
