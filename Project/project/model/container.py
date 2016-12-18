# -*- coding: utf-8 -*-
"""
Docker container related model.

"""
from ming import schema as s
from ming.odm import FieldProperty, ForeignIdProperty, RelationProperty
from ming.odm.declarative import MappedClass

from project.model import DBSession
from project.model import User


class Container(MappedClass):
    """
    Container definition.
    """
    class __mongometa__:
        session = DBSession
        name = 'containers'

    _id = FieldProperty(s.ObjectId)
    container_id = FieldProperty(s.String, required=True)
    datetime_of_creation = FieldProperty(s.datetime, required=True)
    datetime_of_launch = FieldProperty(s.datetime, required=True)
    _user = ForeignIdProperty(User, required=True)
    user = RelationProperty(User)
    status = FieldProperty(s.String, required=True)
    port = FieldProperty(s.Int, required=True)
    host = FieldProperty(s.String, required=True)
    dockerfile_path = FieldProperty(s.String)
    vagrantfile_path = FieldProperty(s.String)
    docker_registry_image_path = FieldProperty(s.String)

__all__ = ['Container']
