# -*- coding: utf-8 -*-
"""Boxes actions controller."""

from tg import expose
from tg.i18n import lazy_ugettext as l_
from tg.exceptions import HTTPFound, HTTPForbidden
from tg.predicates import not_anonymous, has_permission
from tg import request, redirect

from workbox.boxengine import BoxEngine
from workbox.lib.base import BaseController
from workbox import model

__all__ = ['BoxController']


class BoxController(BaseController):
    """Boxes actions controller"""

    # The predicate that must be met for all the actions in this controller:
    allow_only = not_anonymous(msg=l_('Only for authorized users'))

    @expose()
    def index(self):
        """Not used. Just redirect."""

        redirect('/box/new/')

    @expose('workbox.templates.box.new')
    def new(self):
        """Handle the box creation page."""

        return dict(page='new')

    @expose('workbox.templates.box.list')
    def list(self):
        """Handle the box list page."""

        entries = None

        if has_permission('manage'):
            entries = model.Box.get_all_boxes()
        else:
            entries = model.Box.get_all_user_boxes(request.identity['user']._id)

        return dict(page='list', entries=entries)

    @expose()
    def create_from_vagrantfile(self):
        """Create box from given vagrantfile."""

        num_of_copies = int(request.POST['num-of-copies'])
        box_name = request.POST['box-name']

        for _ in range(num_of_copies):
            box_id = BoxEngine.create_box_from_vagrantfile(
                box_name, request.identity['repoze.who.userid'],
                str(request.POST['vagrantfile-text']))

            model.History.add_record(request.identity['repoze.who.userid'],
                                     box_id, 'Создание виртуальной среды #' + str(box_id))

        return HTTPFound(location='/box/list/')

    @expose()
    def create_from_parameters(self):
        """Create box from given parameters."""

        num_of_copies = int(request.POST['num-of-copies'])
        box_name = request.POST['box-name']

        for _ in range(num_of_copies):
            BoxEngine.create_box_from_parameters()

        return HTTPFound(location='/box/list/')

    @expose()
    def start(self):
        """Start box."""

        box_id = int(request.POST['box_id'])

        if not has_permission('manage'):
            if not model.Box.is_author(request.identity['repoze.who.userid'], box_id):
                return HTTPForbidden(
                    'У Вас нет прав доступа для выполнения действий с этой виртуальной средой')

        BoxEngine.start_box(box_id)
        model.History.add_record(request.identity['repoze.who.userid'],
                                 box_id, 'Запуск виртуальной среды #' + str(box_id))

        return HTTPFound(location='/box/list/')

    @expose()
    def stop(self):
        """Stop box."""

        box_id = int(request.POST['box_id'])

        if not has_permission('manage'):
            if not model.Box.is_author(request.identity['repoze.who.userid'], box_id):
                return HTTPForbidden(
                    'У Вас нет прав доступа для выполнения действий с этой виртуальной средой')

        BoxEngine.stop_box(box_id)
        model.History.add_record(request.identity['repoze.who.userid'],
                                 box_id, 'Остановка виртуальной среды #' + str(box_id))

        return HTTPFound(location='/box/list/')

    @expose()
    def copy(self):
        """Copy box."""

        copied_box_id = int(request.POST['box_id'])

        if not has_permission('manage'):
            if not model.Box.is_author(request.identity['repoze.who.userid'], copied_box_id):
                return HTTPForbidden(
                    'У Вас нет прав доступа для выполнения действий с этой виртуальной средой')

        box_id = BoxEngine.copy_box(request.identity['repoze.who.userid'], copied_box_id)
        model.History.add_record(request.identity['repoze.who.userid'],
                                 box_id, 'Копирование виртуальной среды #' +
                                 str(copied_box_id) + ' (создана #' + str(box_id) + ')')

        return HTTPFound(location='/box/list/')

    @expose()
    def delete(self):
        """Delete box."""

        box_id = int(request.POST['box_id'])

        if not has_permission('manage'):
            if not model.Box.is_author(request.identity['repoze.who.userid'], box_id):
                return HTTPForbidden(
                    'У Вас нет прав доступа для выполнения действий с этой виртуальной средой')

        BoxEngine.delete_box(box_id)
        model.History.add_record(request.identity['repoze.who.userid'],
                                 None, 'Удаление виртуальной среды #' + str(box_id))

        return HTTPFound(location='/box/list/')
