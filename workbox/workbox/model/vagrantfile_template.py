# -*- coding: utf-8 -*-
"""Vagrantfile template related model"""

from ming import schema as s
from ming.odm import FieldProperty
from ming.odm.declarative import MappedClass

from workbox.model import DBSession

__all__ = ['VagrantfileTemplate']


class VagrantfileTemplate(MappedClass):
    """
    Vagrantfile template definition

    """

    class __mongometa__:
        session = DBSession
        name = 'vagrantfile_template'

    _id = FieldProperty(s.ObjectId)
    name = FieldProperty(s.String)
    template = FieldProperty(s.String)

    @staticmethod
    def get_all():
        """
        Get all avaliable boxes

        Returns:
            Collection of all vagrantfile templates

        """

        return VagrantfileTemplate.query.find()
