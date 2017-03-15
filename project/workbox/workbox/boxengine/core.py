# -*- coding: utf-8 -*-
"""
Core of box engine package.

"""

import os
import uuid
from datetime import datetime

import vagrant

from workbox import model
from workbox.config.app_cfg import base_config


class BoxEngine():
    """Helper class for work with boxes."""

    base_vagrantfile_directory = '/tmp/workbox/'

    def get_all_boxes(self):
        """Get all boxes from db."""
        return model.Box.query.find()

    def create_box_from_vagrantfile(self, identity, vagrantfile_data):
        """Create box from givent Vagrantfile text."""
        box_name = self._get_box_name_from_vagrantfile(vagrantfile_data)
        vagrantfile_path = self._create_vagrantfile(vagrantfile_data)

        # add to db
        box = model.Box()
        box.box_id = model.AutoincId.get_next_id('box')
        box.user = base_config.sa_auth.user_class.query.get(user_name=identity['repoze.who.userid'])
        box.datetime_of_creation = datetime.now()
        box.datetime_of_modify = box.datetime_of_creation
        box.status = 'created'
        box.name = box_name
        box.vagrantfile_path = vagrantfile_path

        model.DBSession.flush()
        model.DBSession.clear()

    def create_box_from_parameters(self, identity):
        """Create box from givent parameters."""
        pass

    def _create_vagrantfile(self, vagrantfile_data):
        """Create Vagrantfile and return its path."""

        directory = self.base_vagrantfile_directory + str(uuid.uuid4())
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_path = os.path.join(directory, 'Vagrantfile')
        temp_file_path = file_path + '~'

        with open(temp_file_path, 'wb') as output_file:
            output_file.write(vagrantfile_data)

        os.rename(temp_file_path, file_path)

        return file_path

    def _get_box_name_from_vagrantfile(self, vagrantfile_data):
        """Return box name from Vagrantfile."""

        return ''
