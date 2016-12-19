# -*- coding: utf-8 -*-
"""Main Controller"""

import os
import shutil
import uuid
import vagrant
from fabric.api import local
from fabric.context_managers import lcd
from datetime import datetime
from project.config.app_cfg import *
from bson.objectid import ObjectId
from tg import expose, flash, require, url, lurl
from tg import request, redirect, tmpl_context
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.exceptions import HTTPFound
from tg import predicates
from project import model
from project.controllers.secure import SecureController
from tgext.admin.mongo import BootstrapTGMongoAdminConfig as TGAdminConfig
from tgext.admin.controller import AdminController

from tw2.forms import DataGrid

from project.lib.base import BaseController
from project.controllers.error import ErrorController


__all__ = ['RootController']

addressbook_grid = DataGrid(fields=[
    ('Name', 'container_id'),
    ('Surname', 'vagrantfile_path')
])


class RootController(BaseController):
    """
    The root controller for the Project application.

    All the other controllers and WSGI applications should be mounted on this
    controller. For example::

        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()

    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.

    """
    secc = SecureController()
    admin = AdminController(model, None, config_type=TGAdminConfig)

    error = ErrorController()

    def _before(self, *args, **kw):
        tmpl_context.project_name = "project"

    @expose('project.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict(page='index')

    @expose('project.templates.add')
    @require(predicates.not_anonymous(msg=l_('Only for authorized users')))
    def add(self):
        """Handle the 'add' page."""
        return dict(page='add')

    @expose()
    @require(predicates.not_anonymous(msg=l_('Only for authorized users')))
    def start(self, c_id):
        c = model.Container.query.get(_id=ObjectId(c_id))

        v = vagrant.Vagrant(c.vagrantfile_path)
        v.up()

        with lcd(c.vagrantfile_path):
            str_id = local('vagrant docker-exec default -- cat /etc/hostname', capture=True)
        print(str_id)
        c_id = str_id.split(':')[1].strip()

        c1 = model.Container()
        c1.container_id = c_id
        c1.user = base_config.sa_auth.user_class.query.get(user_name=request.identity['repoze.who.userid'])
        c1.datetime_of_creation = c.datetime_of_creation
        c1.datetime_of_launch = datetime.now()
        c1.vagrantfile_path = c.vagrantfile_path
        c1.port = int(c.port)
        c1.status = 'started'
        model.DBSession.flush()
        model.DBSession.clear()

        flash(_('Successfully start container!'))
        return HTTPFound(location='/containers')

    @expose()
    @require(predicates.not_anonymous(msg=l_('Only for authorized users')))
    def stop(self, c_id):
        c = model.Container.query.get(_id=ObjectId(c_id))

        v = vagrant.Vagrant(c.vagrantfile_path)
        v.destroy()

        c1 = model.Container()
        c1.container_id = c.container_id
        c1.user = base_config.sa_auth.user_class.query.get(user_name=request.identity['repoze.who.userid'])
        c1.datetime_of_creation = c.datetime_of_creation
        c1.datetime_of_launch = c1.datetime_of_launch
        c1.vagrantfile_path = c.vagrantfile_path
        c1.port = int(c.port)
        c1.status = 'stopped'
        model.DBSession.flush()
        model.DBSession.clear()
        flash(_('Successfully stopped container!'))
        return HTTPFound(location='/containers')

    @expose()
    @require(predicates.not_anonymous(msg=l_('Only for authorized users')))
    def addnew(self):
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

        c = model.Container()
        c.user = base_config.sa_auth.user_class.query.get(user_name=request.identity['repoze.who.userid'])
        c.datetime_of_creation = datetime.now()
        c.vagrantfile_path = directory
        c.status = 'created'
        c.port = int(request.POST['textinput'])
        model.DBSession.flush()
        model.DBSession.clear()

        flash(_('Successfully add new continer!'))
        return HTTPFound(location='/add')

    @expose('project.templates.logs')
    def logs(self):
        """This method showcases TG's access to the wsgi environment."""
        return dict(page='logs')

    @expose('project.templates.containers')
    def containers(self):
        entries = model.Container.query.find()
        return dict(page='containers', entries=entries)

    @expose('project.templates.index')
    @require(predicates.has_permission('manage', msg=l_('Only for managers')))
    def admins_permission_only(self, **kw):
        """Illustrate how a page for manager only works."""
        return dict(page='managers stuff')

    @expose('project.templates.index')
    @require(predicates.is_user('teacher', msg=l_('Only for the teacher')))
    def teacher_user_only(self, **kw):
        """Illustrate how a page exclusive for the teacher works."""
        return dict(page='teacher stuff')

    @expose('project.templates.login')
    def login(self, came_from=lurl('/'), failure=None, login=''):
        """Start the user login."""
        if failure is not None:
            if failure == 'user-not-found':
                flash(_('User not found'), 'error')
            elif failure == 'invalid-password':
                flash(_('Invalid Password'), 'error')

        login_counter = request.environ.get('repoze.who.logins', 0)
        if failure is None and login_counter > 0:
            flash(_('Wrong credentials'), 'warning')

        return dict(page='login', login_counter=str(login_counter),
                    came_from=came_from, login=login)

    @expose()
    def post_login(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.

        """
        if not request.identity:
            login_counter = request.environ.get('repoze.who.logins', 0) + 1
            redirect('/login',
                     params=dict(came_from=came_from, __logins=login_counter))
        userid = request.identity['repoze.who.userid']
        flash(_('Welcome back, %s!') % userid)

        # Do not use tg.redirect with tg.url as it will add the mountpoint
        # of the application twice.
        return HTTPFound(location=came_from)

    @expose()
    def post_logout(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.

        """
        flash(_('We hope to see you soon!'))
        return HTTPFound(location=came_from)
