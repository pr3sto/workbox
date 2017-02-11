# -*- coding: utf-8 -*-
"""Boxes actions controller."""

import os
import shutil
import uuid
import vagrant
from fabric.api import local
from fabric.context_managers import lcd
from bson.objectid import ObjectId
from tg import expose
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.exceptions import HTTPFound
from tg.predicates import not_anonymous
from tg import request, redirect
from workbox import model
from workbox.config.app_cfg import base_config
from datetime import datetime

from workbox.lib.base import BaseController

__all__ = ['BoxController']


class BoxController(BaseController):
    """Boxes actions controller"""

    # The predicate that must be met for all the actions in this controller:
    allow_only = not_anonymous(msg=l_('Only for authorized users'))

    @expose()
    def index(self):
        redirect('/box/new')

    @expose('workbox.templates.box_new')
    def new(self):
        return dict(page='box_new')

    @expose()
    def create(self):
        input_file = request.POST['filebutton'].file
        directory = '/tmp/project_bsc/' + str(uuid.uuid4())

        if not os.path.exists(directory):
            os.makedirs(directory)

        file_path = os.path.join(directory, 'Vagrantfile')
        temp_file_path = file_path + '~'

        input_file.seek(0)
        with open(temp_file_path, 'wb') as output_file:
            shutil.copyfileobj(input_file, output_file)

        os.rename(temp_file_path, file_path)

        c = model.Box()
        c.user = base_config.sa_auth.user_class.query.get(user_name=request.identity['repoze.who.userid'])
        c.datetime_of_creation = datetime.now()
        c.vagrantfile_path = directory
        c.status = 'created'
        c.port = int(request.POST['textinput'])
        model.DBSession.flush()
        model.DBSession.clear()

        return HTTPFound(location='/box/new')

    @expose('workbox.templates.box_list')
    def list(self):
        entries = model.Box.query.find()
        return dict(page='box_list', entries=entries)

    @expose()
    def start(self, c_id):
        c = model.Box.query.get(_id=ObjectId(c_id))

        v = vagrant.Vagrant(c.vagrantfile_path)
        v.up()

        with lcd(c.vagrantfile_path):
            str_id = local('vagrant docker-exec default -- cat /etc/hostname', capture=True)
        print(str_id)
        c_id = str_id.split(':')[1].strip()

        c1 = model.Box()
        c1.container_id = c_id
        c1.user = base_config.sa_auth.user_class.query.get(user_name=request.identity['repoze.who.userid'])
        c1.datetime_of_creation = c.datetime_of_creation
        c1.datetime_of_launch = datetime.now()
        c1.vagrantfile_path = c.vagrantfile_path
        c1.port = int(c.port)
        c1.status = 'started'
        model.DBSession.flush()
        model.DBSession.clear()

        return HTTPFound(location='/containers') # TODO

    @expose()
    def stop(self, c_id):
        c = model.Box.query.get(_id=ObjectId(c_id))

        v = vagrant.Vagrant(c.vagrantfile_path)
        v.destroy()

        c1 = model.Box()
        c1.container_id = c.container_id
        c1.user = base_config.sa_auth.user_class.query.get(user_name=request.identity['repoze.who.userid'])
        c1.datetime_of_creation = c.datetime_of_creation
        c1.datetime_of_launch = c1.datetime_of_launch
        c1.vagrantfile_path = c.vagrantfile_path
        c1.port = int(c.port)
        c1.status = 'stopped'
        model.DBSession.flush()
        model.DBSession.clear()
        return HTTPFound(location='/containers') # TODO
