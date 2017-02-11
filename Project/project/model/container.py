# -*- coding: utf-8 -*-
"""
Docker container related model.

"""

from ming import schema as s
from ming.odm import FieldProperty, ForeignIdProperty, RelationProperty
from ming.odm.declarative import MappedClass

from project.model import DBSession
from project.model import User

__all__ = ['Container']


class Container(MappedClass):
    """
    Container definition.

    """
    class __mongometa__:
        session = DBSession
        name = 'containers'

    _id = FieldProperty(s.ObjectId)
    container_id = FieldProperty(s.String)

    datetime_of_creation = FieldProperty(s.datetime)
    datetime_of_launch = FieldProperty(s.datetime)

    _user = ForeignIdProperty(User)
    user = RelationProperty(User)

    status = FieldProperty(s.String)

    host = FieldProperty(s.String)
    port = FieldProperty(s.Int)
    dockerfile_path = FieldProperty(s.String)
    vagrantfile_path = FieldProperty(s.String)

    docker_registry_image_path = FieldProperty(s.String)
