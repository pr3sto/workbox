# -*- coding: utf-8 -*-
"""Virtual environment (box) related model"""

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
            user_name (string): user name
            box_name (string): name of new box
            vagrantfile_path (string): path to vagrantfile\

        Returns:
            Id of created box

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

        return box.box_id

    @staticmethod
    def is_author(user_name, box_id):
        """
        Detect is user author of box

        Args:
            user_name (string): user name

        Returns:
            True if user is author, otherwise - False

        """

        box = Box.get_by_box_id(box_id)
        if box.user == User.query.get(user_name=user_name):
            return True
        else:
            return False

    @staticmethod
    def get_by_box_id(box_id):
        """
        Get box with given box_id

        Args:
            box_id (int): box_id in db

        Returns:
            Box

        """

        return Box.query.get(box_id=box_id)

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

        Args:
            status (string): box's status

        Returns:
            Number of all boxes

        """

        return Box.query.find({'status': status}).count()

    @staticmethod
    def change_status(box_id, status):
        """
        Change status of box

        Args:
            box_id (int): box_id in db
            status (string): box's new status

        """

        box = Box.get_by_box_id(box_id)
        box.status = status
        box.datetime_of_modify = datetime.now()

        DBSession.flush()
        DBSession.clear()
