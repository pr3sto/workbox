# -*- coding: utf-8 -*-
"""Virtual working environment (box) related model"""

from datetime import datetime

from ming import schema as s
from ming.odm import FieldProperty, ForeignIdProperty, RelationProperty
from ming.odm.declarative import MappedClass

from workbox.model import DBSession
from workbox.model import User, Counter

__all__ = ['Box']


class Box(MappedClass):
    """
    Box definition

    """
    
    class __mongometa__:
        session = DBSession
        name = 'box'

    _id = FieldProperty(s.ObjectId)
    box_id = FieldProperty(s.Int)

    datetime_of_creation = FieldProperty(s.datetime)
    datetime_of_modify = FieldProperty(s.datetime)

    _user_id = ForeignIdProperty(User)
    user = RelationProperty(User)

    status = FieldProperty(s.String)
    name = FieldProperty(s.String)
    vagrantfile_path = FieldProperty(s.String)

    @staticmethod
    def add_new_box(user_name, box_name, vagrantfile_path):
        """
        Add new box to db

        Args:
            user_name (string): name of user
            box_name (string): name of new box
            vagrantfile_path (string): path to vagrantfile

        """

        box = Box()
        box.box_id = Counter.get_next_id('box')
        box.user = User.query.get(user_name=user_name)
        box.datetime_of_creation = datetime.now()
        box.datetime_of_modify = box.datetime_of_creation
        box.status = 'created'
        box.name = box_name
        box.vagrantfile_path = vagrantfile_path

        DBSession.flush()
        DBSession.clear()

    @staticmethod
    def get_all_user_boxes(user_id):
        """
        Get all user boxes from db

        Args:
            user_id (int): user id in db

        Returns:
            Collection of all boxes

        """

        return Box.query.find({'_user_id': user_id})

    @staticmethod
    def get_all_boxes():
        """
        Get all boxes from db

        Returns:
            Collection of all boxes

        """

        return Box.query.find()

    @staticmethod
    def get_number_of_user_boxes(user_id, status):
        """
        Get number of all users boxes with given status from db

        Args:
            user_id (int): user id in db
            status (string): box's status

        Returns:
            Number of all user's boxes

        """

        return Box.query.find({'status': status, '_user_id': user_id}).count()

    @staticmethod
    def get_number_of_all_boxes(status):
        """
        Get number of all boxes with given status from db

        Returns:
            Number of all boxes
            status (string): box's status

        """

        return Box.query.find({'status': status}).count()
