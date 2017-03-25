# -*- coding: utf-8 -*-
"""Core of box engine package"""

import os
import uuid

import vagrant

from workbox import model


class BoxEngine(object):
    """Helper class for working with boxes"""

    base_vagrantfile_directory = '/tmp/workbox/'

    @staticmethod
    def create_box_from_vagrantfile(box_name, user_name, vagrantfile_data):
        """
        Create box from givent Vagrantfile text

        Args:
            box_name (string): name of box
            user_name (string): author name
            vagrantfile_data (string): text data of vagrantfile

        """

        vagrantfile_path = BoxEngine._create_vagrantfile(vagrantfile_data)
        model.Box.add_new_box(user_name, box_name, vagrantfile_path)

    @staticmethod
    def create_box_from_parameters():
        """
        Create box from givent parameters

        Args:
            box_name (string): name of box
            user_name (string): author name

        """

        pass

    @staticmethod
    def get_service_load_value():
        """
        Get service load value

        Returns:
            Service load value (int between 0 and 100)

        """

        import random
        return random.randint(0, 100)

    @staticmethod
    def get_number_of_user_boxes(user_id):
        """
        Get number of all users boxes from db

        Args:
            user_id (int): user id in db

        Returns:
            Number of all user's boxes

        """

        my_boxes = {}
        my_boxes['created'] = model.Box.get_number_of_user_boxes(user_id, 'created')
        my_boxes['started'] = model.Box.get_number_of_user_boxes(user_id, 'started')
        my_boxes['stopped'] = model.Box.get_number_of_user_boxes(user_id, 'stopped')

        return my_boxes

    @staticmethod
    def get_number_of_all_boxes():
        """
        Get number of all boxes from db

        Returns:
            Number of all boxes

        """

        all_boxes = {}
        all_boxes['created'] = model.Box.get_number_of_all_boxes('created')
        all_boxes['started'] = model.Box.get_number_of_all_boxes('started')
        all_boxes['stopped'] = model.Box.get_number_of_all_boxes('stopped')

        return all_boxes

    @staticmethod
    def get_service_load_chart_data():
        """
        Get service load chart data for week

        Returns:
            Chart data

        """

        chart_data = {}
        chart_data['labels'] = ['Пн', 'Вт', 'Ср', 'Чтв', 'Пт', 'Сб', 'Вск']
        chart_data['data'] = [65, 59, 56, 44, 38, 5, 5]

        return chart_data

    @staticmethod
    def _create_vagrantfile(vagrantfile_data):
        """
        Create Vagrantfile and return its path

        Args:
            vagrantfile_data (string): text data of vagrantfile

        Returns:
            Path to created vagrantfile

        """

        directory = BoxEngine.base_vagrantfile_directory + str(uuid.uuid4())
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_path = os.path.join(directory, 'Vagrantfile')
        temp_file_path = file_path + '~'

        with open(temp_file_path, 'wb') as output_file:
            output_file.write(vagrantfile_data)

        os.rename(temp_file_path, file_path)

        return file_path
