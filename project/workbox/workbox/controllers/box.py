# -*- coding: utf-8 -*-
"""Boxes actions controller."""

import json

from tg import expose
from tg.i18n import lazy_ugettext as l_
from tg.exceptions import HTTPFound, HTTPForbidden, HTTPServerError
from tg.predicates import not_anonymous, has_permission
from tg import request, redirect

from workbox import model
from workbox.boxengine import BoxEngine
from workbox.lib.base import BaseController
from workbox.lib.helpers import get_hostname

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

        templates = model.VagrantfileTemplate.get_all()

        return dict(page='new', templates=templates)

    @expose('workbox.templates.box.list')
    def list(self):
        """Handle the box list page."""

        has_boxes = False

        if has_permission('manage'):
            all_boxes = BoxEngine.get_number_of_all_boxes()
            if all_boxes['created'] > 0 or all_boxes['stopped'] or all_boxes['started']:
                has_boxes = True
        else:
            my_boxes = BoxEngine.get_number_of_user_boxes(request.identity['user']._id)
            if my_boxes['created'] > 0 or my_boxes['stopped'] or my_boxes['started']:
                has_boxes = True

        print has_boxes

        return dict(page='list', has_boxes=has_boxes)

    @expose('workbox.templates.box.id')
    def id(self, box_id):
        """Handle the box page."""

        box_id = int(box_id)

        try:
            if not has_permission('manage'):
                if not BoxEngine.is_author(request.identity['repoze.who.userid'], box_id):
                    return HTTPForbidden(
                        'У Вас нет прав доступа для выполнения действий с этой виртуальной средой')

            box = BoxEngine.get_box_by_id(box_id)
            if box is None:
                raise IndexError("Виртуальная среда не найдена")

            vagrantfile = BoxEngine.get_vagrantfile_data(box_id)
            host = get_hostname()
        except Exception as ex:
            return HTTPServerError(ex.message)

        return dict(page='id', box=box, vagrantfile=vagrantfile, host=host)

    @expose()
    def create_from_vagrantfile(self):
        """Create box from given vagrantfile."""

        num_of_copies = int(request.POST['num-of-copies'])
        box_name = request.POST['box-name']
        vagrantfile = request.POST['vagrantfile-text']

        for _ in range(num_of_copies):
            box_id = BoxEngine.create_box_from_vagrantfile(
                box_name, request.identity['repoze.who.userid'], str(vagrantfile))

            model.History.add_record(request.identity['repoze.who.userid'],
                                     box_id, 'Создание виртуальной среды #' + str(box_id))

        return HTTPFound(location='/box/list/')

    @expose()
    def create_from_parameters(self):
        """Create box from given parameters."""

        num_of_copies = int(request.POST['num-of-copies'])
        box_name = request.POST['box-name']
        vagrantfile = request.POST['vagrantfile-text']

        for _ in range(num_of_copies):
            box_id = BoxEngine.create_box_from_parameters(
                box_name, request.identity['repoze.who.userid'], str(vagrantfile))

            model.History.add_record(request.identity['repoze.who.userid'],
                                     box_id, 'Создание виртуальной среды #' + str(box_id))

        return HTTPFound(location='/box/list/')

    @expose()
    def get(self):
        """Returns boxes data."""

        entries = None
        data = []

        if has_permission('manage'):
            entries = BoxEngine.get_all_boxes()

            for entry in entries:
                box = []
                box.append(entry.box_id)
                box.append(entry.name)
                box.append(entry.status)
                box.append(entry.user.display_name)
                box.append(entry.datetime_of_creation.strftime("%Y-%m-%d %H:%M"))
                box.append(entry.datetime_of_modify.strftime("%Y-%m-%d %H:%M"))
                box.append(None)
                data.append(box)
        else:
            entries = BoxEngine.get_all_user_boxes(request.identity['user']._id)

            for entry in entries:
                box = []
                box.append(entry.box_id)
                box.append(entry.name)
                box.append(entry.status)
                box.append(entry.datetime_of_creation.strftime("%Y-%m-%d %H:%M"))
                box.append(entry.datetime_of_modify.strftime("%Y-%m-%d %H:%M"))
                box.append(None)
                data.append(box)

        json_entries = {}
        json_entries['data'] = data
        return json.dumps(json_entries)

    @expose()
    def update_status(self):
        """Update status of boxes."""

        pass

    @expose()
    def start(self, box_id):
        """Start box."""

        box_id = int(box_id)

        try:
            if not has_permission('manage'):
                if not BoxEngine.is_author(request.identity['repoze.who.userid'], box_id):
                    return HTTPForbidden(
                        'У Вас нет прав доступа для выполнения действий с этой виртуальной средой')

            BoxEngine.start_box(box_id)
            model.History.add_record(request.identity['repoze.who.userid'],
                                     box_id, 'Запуск виртуальной среды #' + str(box_id))
        except Exception as ex:
            return HTTPServerError(ex.message)

    @expose()
    def stop(self, box_id):
        """Stop box."""
        
        box_id = int(box_id)

        try:
            if not has_permission('manage'):
                if not BoxEngine.is_author(request.identity['repoze.who.userid'], box_id):
                    return HTTPForbidden(
                        'У Вас нет прав доступа для выполнения действий с этой виртуальной средой')

            BoxEngine.stop_box(box_id)
            model.History.add_record(request.identity['repoze.who.userid'],
                                     box_id, 'Остановка виртуальной среды #' + str(box_id))
        except Exception as ex:
            return HTTPServerError(ex.message)

    @expose()
    def copy(self, copied_box_id):
        """Copy box."""

        copied_box_id = int(copied_box_id)

        try:
            if not has_permission('manage'):
                if not BoxEngine.is_author(request.identity['repoze.who.userid'], copied_box_id):
                    return HTTPForbidden(
                        'У Вас нет прав доступа для выполнения действий с этой виртуальной средой')

            box_id = BoxEngine.copy_box(request.identity['repoze.who.userid'], copied_box_id)
            model.History.add_record(request.identity['repoze.who.userid'],
                                     box_id, 'Копирование виртуальной среды #' +
                                     str(copied_box_id) + ' (создана #' + str(box_id) + ')')
        except Exception as ex:
            return HTTPServerError(ex.message)

    @expose()
    def delete(self, box_id):
        """Delete box."""

        box_id = int(box_id)

        try:
            if not has_permission('manage'):
                if not BoxEngine.is_author(request.identity['repoze.who.userid'], box_id):
                    return HTTPForbidden(
                        'У Вас нет прав доступа для выполнения действий с этой виртуальной средой')

            BoxEngine.delete_box(box_id)
            model.History.add_record(request.identity['repoze.who.userid'],
                                     None, 'Удаление виртуальной среды #' + str(box_id))
        except Exception as ex:
            return HTTPServerError(ex.message)

    @expose()
    def update_vagrantfile(self, box_id, vagrantfile_text):
        """Update vagrantfile."""

        box_id = int(box_id)

        try:
            if not has_permission('manage'):
                if not BoxEngine.is_author(request.identity['repoze.who.userid'], box_id):
                    return HTTPForbidden(
                        'У Вас нет прав доступа для выполнения действий с этой виртуальной средой')

            BoxEngine.update_vagrantfile(box_id, vagrantfile_text)
            model.History.add_record(request.identity['repoze.who.userid'],
                                     box_id,
                                     'Изменение Vagrantfile виртуальной среды #' + str(box_id))

            return BoxEngine.get_vagrantfile_data(box_id)

        except Exception as ex:
            return HTTPServerError(ex.message)
