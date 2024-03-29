# -*- coding: utf-8 -*-
"""
Auth* related model

This is where the models used by the authentication stack are defined

"""

import os
from datetime import datetime
from hashlib import sha256

from ming import schema as s
from ming.odm import FieldProperty, ForeignIdProperty, RelationProperty
from ming.odm.declarative import MappedClass
from workbox.model import DBSession

__all__ = ['User', 'Group', 'Permission']


class Group(MappedClass):
    """
    Group definition
    """

    class __mongometa__:
        session = DBSession
        name = 'group'
        unique_indexes = [('group_name',),]

    _id = FieldProperty(s.ObjectId)
    group_name = FieldProperty(s.String)
    display_name = FieldProperty(s.String)

    permissions = RelationProperty('Permission')


class Permission(MappedClass):
    """
    Permission definition
    """

    class __mongometa__:
        session = DBSession
        name = 'permission'
        unique_indexes = [('permission_name',),]

    _id = FieldProperty(s.ObjectId)
    permission_name = FieldProperty(s.String)
    description = FieldProperty(s.String)

    _groups = ForeignIdProperty(Group, uselist=True)
    groups = RelationProperty(Group)


class User(MappedClass):
    """
    User definition

    This is the user definition used by :mod:`repoze.who`, which requires at
    least the ``user_name`` column.

    """

    class __mongometa__:
        session = DBSession
        name = 'user'
        unique_indexes = [('user_name',),]

    class PasswordProperty(FieldProperty):
        @classmethod
        def _hash_password(cls, password):
            salt = sha256()
            salt.update(os.urandom(60))
            salt = salt.hexdigest()

            hash = sha256()
            hash.update((password + salt).encode('utf-8'))
            hash = hash.hexdigest()

            password = salt + hash
            password = password.decode('utf-8')

            return password

        def __set__(self, instance, value):
            value = self._hash_password(value)
            return FieldProperty.__set__(self, instance, value)

    _id = FieldProperty(s.ObjectId)
    user_name = FieldProperty(s.String)
    display_name = FieldProperty(s.String)

    _groups = ForeignIdProperty(Group, uselist=True)
    groups = RelationProperty(Group)

    password = PasswordProperty(s.String)
    created = FieldProperty(s.DateTime, if_missing=datetime.now)

    @property
    def permissions(self):
        """Get all user's permissions"""

        return Permission.query.find(dict(_groups={'$in': self._groups})).all()

    def validate_password(self, password):
        """
        Check the password against existing credentials.

        :param password: the password that was provided by the user to
            try and authenticate. This is the clear text version that we will
            need to match against the hashed one in the database.
        :type password: unicode object.
        :return: Whether the password is valid.
        :rtype: bool

        """

        hash = sha256()
        hash.update((password + self.password[:64]).encode('utf-8'))
        return self.password[64:] == hash.hexdigest()
