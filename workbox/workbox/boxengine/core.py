# -*- coding: utf-8 -*-
"""Core of box engine package"""

import os
import shutil
import uuid
import string
from subprocess import CalledProcessError
import vagrant

from workbox import model
from workbox.lib.helpers import get_vagrantfiles_base_folder, get_free_port, get_server_load_value


class BoxEngine(object):
    """Helper class for work with boxes"""

    @staticmethod
    def get_all_boxes():
        """
        Get all boxes from db

        Returns:
            Collection of all boxes

        """

        return model.Box.get_all_boxes()

    @staticmethod
    def get_all_user_boxes(user_id):
        """
        Get all user boxes from db

        Args:
            user_id (int): user id in db

        Returns:
            Collection of all boxes

        """

        return model.Box.get_all_user_boxes(user_id)

    @staticmethod
    def get_box_by_id(box_id):
        """
        Get box with given box_id

        Args:
            box_id (int): box_id in db

        Returns:
            model.Box or None

        """

        return model.Box.get_by_box_id(box_id)

    @staticmethod
    def is_author(user_name, box_id):
        """
        Detect is user author of box

        Args:
            user_name (string): user name
            box_id (int): id of box

        Raises:
            IndexError: no box with given box_id

        Returns:
            True if user is author, otherwise - False

        """

        return model.Box.is_author(user_name, box_id)

    @staticmethod
    def update_vagrantfile(box_id, vagrantfile_data):
        """
        Update Vagrantfile of box with given box_id

        Args:
            box_id (int): id of box
            vagrantfile_data (string): text data of vagrantfile

        Raises:
            IndexError: no box with given box_id
            EnvironmentError: vagrantfile was removed

        """

        box = BoxEngine.get_box_by_id(box_id)
        if box is None:
            raise IndexError("Виртуальная среда #" + str(box_id) + " не найдена")

        file_path = os.path.join(box.vagrantfile_path, 'Vagrantfile')

        if not os.path.exists(file_path):
            raise EnvironmentError("Vagrantfile был удален (#" + str(box_id) + ")")

        with open(file_path, 'wb') as v_file:
            v_file.write(vagrantfile_data)

        try:
            model.Box.update_datetime_of_modify(box_id)
        except IndexError:
            raise

    @staticmethod
    def create_box_from_vagrantfile(box_name, user_name, vagrantfile_data):
        """
        Create box from givent Vagrantfile text

        Args:
            box_name (string): name of box
            user_name (string): user name
            vagrantfile_data (string): text data of vagrantfile

        Returns:
            Id of created box

        """

        port = None
        if '#FPRT#' in vagrantfile_data:
            while True:
                port = get_free_port()
                if model.Box.is_port_free(port):
                    vagrantfile_data = string.replace(vagrantfile_data, '#FPRT#', str(port))
                    break

        vagrantfile_path = BoxEngine._create_vagrantfile(vagrantfile_data)
        box_id = model.Box.add_new_box(user_name, box_name, port, vagrantfile_path)
        return box_id

    @staticmethod
    def create_box_from_parameters(box_name, user_name, vagrantfile_data):
        """
        Create box from givent parameters

        Args:
            box_name (string): name of box
            user_name (string): user name
            vagrantfile_data (string): text data of vagrantfile

        """

        return BoxEngine.create_box_from_vagrantfile(box_name, user_name, vagrantfile_data)

    @staticmethod
    def update_all_boxes_status():
        """
        Update status of all boxes

        Raises:
            EnvironmentError: vagrant failed

        """

        boxes = BoxEngine.get_all_boxes()
        status = None

        for box in boxes:
            try:
                vagrant_box = vagrant.Vagrant(box.vagrantfile_path)
                status = vagrant_box.status()
            except CalledProcessError:
                raise EnvironmentError(
                    "Не удалось выполнить 'vagrant status' (#" + str(box.box_id) + ")")
            except OSError:
                raise EnvironmentError(
                    "Не удалось выполнить 'vagrant status' (проблема с доступом к Vagrantfile) (#"
                    + str(box.box_id) + ")")

            if status is not None and len(status) > 0 and status[0].state is not None:
                if box.status == 'started' and status[0].state != 'running':
                    model.Box.change_status(box.box_id, 'stopped')
                if box.status != 'started' and status[0].state == 'running':
                    model.Box.change_status(box.box_id, 'started')

    @staticmethod
    def update_all_user_boxes_status(user_id):
        """
        Update status of user boxes

        Args:
            user_id (int): user id in db

        Raises:
            EnvironmentError: vagrant failed

        """

        boxes = BoxEngine.get_all_user_boxes(user_id)

        for box in boxes:
            try:
                vagrant_box = vagrant.Vagrant(box.vagrantfile_path)
                status = vagrant_box.status()
            except CalledProcessError:
                raise EnvironmentError(
                    "Не удалось выполнить 'vagrant status' (#" + str(box.box_id) + ")")
            except OSError:
                raise EnvironmentError(
                    "Не удалось выполнить 'vagrant status' (проблема с доступом к Vagrantfile) (#"
                    + str(box.box_id) + ")")

            if status is not None and len(status) > 0 and status[0].state is not None:
                if box.status == 'started' and status[0].state != 'running':
                    model.Box.change_status(box.box_id, 'stopped')
                if box.status != 'started' and status[0].state == 'running':
                    model.Box.change_status(box.box_id, 'started')

    @staticmethod
    def start_box(box_id):
        """
        Start box

        Args:
            box_id (int): id of box

        Raises:
            EnvironmentError: vagrant failed
            IndexError: no box with given box_id

        """

        box = BoxEngine.get_box_by_id(box_id)
        if box is None:
            raise IndexError("Виртуальная среда #" + str(box_id) + " не найдена")

        try:
            vagrant_box = vagrant.Vagrant(box.vagrantfile_path)
            vagrant_box.up()
        except CalledProcessError:
            raise EnvironmentError("Не удалось выполнить 'vagrant up' (#" + str(box_id) + ")")
        except OSError:
            raise EnvironmentError(
                "Не удалось выполнить 'vagrant up' (проблема с доступом к Vagrantfile) (#"
                + str(box_id) + ")")

        model.Box.change_status(box_id, 'started')

    @staticmethod
    def stop_box(box_id):
        """
        Stop box

        Args:
            box_id (int): id of box

        Raises:
            IndexError: no box with given box_id
            EnvironmentError: vagrant failed

        """

        box = BoxEngine.get_box_by_id(box_id)
        if box is None:
            raise IndexError("Виртуальная среда #" + str(box_id) + " не найдена")

        try:
            vagrant_box = vagrant.Vagrant(box.vagrantfile_path)
            vagrant_box.destroy()
        except CalledProcessError:
            raise EnvironmentError("Не удалось выполнить 'vagrant destroy' (#" + str(box_id) + ")")
        except OSError:
            raise EnvironmentError(
                "Не удалось выполнить 'vagrant destroy' (проблема с доступом к Vagrantfile) (#"
                + str(box_id) + ")")

        model.Box.change_status(box_id, 'stopped')

    @staticmethod
    def copy_box(user_name, copied_box_id):
        """
        Copy box from box with given box_id

        Args:
            user_name (string): user name
            copied_box_id (int): id of copied box

        Returns:
            Id of created box

        Raises:
            IndexError: no box with given box_id
            EnvironmentError: vagrantfile was removed

        """

        copied_box = BoxEngine.get_box_by_id(copied_box_id)
        if copied_box is None:
            raise IndexError("Виртуальная среда #" + str(copied_box_id) + " не найдена")

        port = None
        if copied_box.port != None:
            while True:
                port = get_free_port()
                if model.Box.is_port_free(port):
                    break

        file_path = os.path.join(copied_box.vagrantfile_path, 'Vagrantfile')

        if not os.path.exists(file_path):
            raise EnvironmentError("Vagrantfile был удален (#" + str(copied_box_id) + ")")

        with open(file_path, 'r') as v_file:
            vagrantfile_path = BoxEngine._create_vagrantfile(v_file.read())
            box_id = model.Box.add_new_box(user_name, copied_box.name, port, vagrantfile_path)
            return box_id

    @staticmethod
    def delete_box(box_id):
        """
        Delete box with given box_id

        Args:
            box_id (int): id of box

        Raises:
            IndexError: no box with given box_id

        """

        box = BoxEngine.get_box_by_id(box_id)
        if box is None:
            raise IndexError("Виртуальная среда #" + str(box_id) + " не найдена")

        if box.status == 'started':
            BoxEngine.stop_box(box_id)

        vagrantfile_path = box.vagrantfile_path

        model.Box.delete_box(box_id)
        BoxEngine._delete_vagrantfile(vagrantfile_path)

    @staticmethod
    def get_vagrantfile_data(box_id):
        """
        Return vagrantfile data of box

        Args:
            box_id (int): id of box

        Returns:
            Vagrantfile data

        Raises:
            IndexError: no box with given box_id
            EnvironmentError: vagrantfile was removed

        """

        box = BoxEngine.get_box_by_id(box_id)
        if box is None:
            raise IndexError("Виртуальная среда #" + str(box_id) + " не найдена")


        file_path = os.path.join(box.vagrantfile_path, 'Vagrantfile')

        if not os.path.exists(file_path):
            raise EnvironmentError("Vagrantfile был удален (#" + str(box_id) + ")")

        with open(file_path, 'r') as v_file:
            return v_file.read()

    @staticmethod
    def get_server_load_value():
        """
        Get server load value

        Returns:
            Server load value (int between 0 and 100)

        """

        return get_server_load_value()

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
    def _create_vagrantfile(vagrantfile_data):
        """
        Create Vagrantfile and return its path

        Args:
            vagrantfile_data (string): text data of vagrantfile

        Returns:
            Path to created vagrantfile

        """

        directory = str(get_vagrantfiles_base_folder()) + str(uuid.uuid4())
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_path = os.path.join(directory, 'Vagrantfile')
        temp_file_path = file_path + '~'

        with open(temp_file_path, 'wb') as output_file:
            output_file.write(vagrantfile_data)

        os.rename(temp_file_path, file_path)

        return directory

    @staticmethod
    def _delete_vagrantfile(vagrantfile_dir):
        """
        Delete Vagrantfile from disk

        Args:
            vagrantfile_dir (string): path to vagrantfile

        """

        if os.path.exists(vagrantfile_dir):
            shutil.rmtree(vagrantfile_dir)
