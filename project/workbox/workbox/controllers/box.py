# -*- coding: utf-8 -*-
"""Boxes actions controller."""

from tg import expose
from tg.i18n import lazy_ugettext as l_
from tg.exceptions import HTTPFound
from tg.predicates import not_anonymous
from tg import request, redirect

from workbox.boxengine import BoxEngine
from workbox.lib.base import BaseController

__all__ = ['BoxController']


class BoxController(BaseController):
    """Boxes actions controller"""

    # The predicate that must be met for all the actions in this controller:
    allow_only = not_anonymous(msg=l_('Only for authorized users'))

    # engine for work with boxes
    box_engine = BoxEngine()

    @expose()
    def index(self):
        """Not used. Just redirect."""
        redirect('/box/new')

    @expose('workbox.templates.box.new')
    def new(self):
        """Handle the box creation page."""
        return dict(page='new')

    @expose('workbox.templates.box.list')
    def list(self):
        """Handle the box list page."""
        entries = self.box_engine.get_all_boxes()
        return dict(page='list', entries=entries)

    @expose()
    def create_from_vagrantfile(self):
        """Create box from given vagrantfile."""
        num_of_copies = int(request.POST['num-of-copies'])

        for _ in range(num_of_copies):
            self.box_engine.create_box_from_vagrantfile(
                request.identity, str(request.POST['vagrantfile-text'])
            )

        return HTTPFound(location='/box/list')

    @expose()
    def create_from_parameters(self):
        """Create box from given parameters."""
        num_of_copies = int(request.POST['num-of-copies'])

        for _ in range(num_of_copies):
            self.box_engine.create_box_from_parameters(
                request.identity
            )

        return HTTPFound(location='/box/list')

    @expose()
    def start(self, c_id):
        # c = model.Box.query.get(_id=ObjectId(c_id))
        #
        # v = vagrant.Vagrant(c.vagrantfile_path)
        # v.up()
        #
        # with lcd(c.vagrantfile_path):
        #     str_id = local('vagrant docker-exec default -- cat /etc/hostname', capture=True)
        # print(str_id)
        # c_id = str_id.split(':')[1].strip()
        #
        # c1 = model.Box()
        # c1.container_id = c_id
        # c1.user = base_config.sa_auth.user_class.query.get(user_name=request.identity['repoze.who.userid'])
        # c1.datetime_of_creation = c.datetime_of_creation
        # c1.datetime_of_launch = datetime.now()
        # c1.vagrantfile_path = c.vagrantfile_path
        # c1.port = int(c.port)
        # c1.status = 'started'
        # model.DBSession.flush()
        # model.DBSession.clear()

        return HTTPFound(location='/containers') # TODO

    @expose()
    def stop(self, c_id):
        # c = model.Box.query.get(_id=ObjectId(c_id))
        #
        # v = vagrant.Vagrant(c.vagrantfile_path)
        # v.destroy()
        #
        # c1 = model.Box()
        # c1.container_id = c.container_id
        # c1.user = base_config.sa_auth.user_class.query.get(user_name=request.identity['repoze.who.userid'])
        # c1.datetime_of_creation = c.datetime_of_creation
        # c1.datetime_of_launch = c1.datetime_of_launch
        # c1.vagrantfile_path = c.vagrantfile_path
        # c1.port = int(c.port)
        # c1.status = 'stopped'
        # model.DBSession.flush()
        # model.DBSession.clear()
        return HTTPFound(location='/containers') # TODO
