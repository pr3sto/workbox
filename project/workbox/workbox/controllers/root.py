# -*- coding: utf-8 -*-
"""Main Controller"""

import json

from tg import expose, lurl, require
from tg import request, redirect, tmpl_context
from tg.i18n import lazy_ugettext as l_
from tg.predicates import not_anonymous, has_permission
from tg.exceptions import HTTPFound
from tgext.admin.mongo import BootstrapTGMongoAdminConfig as TGAdminConfig
from tgext.admin.controller import AdminController

from workbox import model
from workbox.lib.base import BaseController
from workbox.controllers.error import ErrorController
from workbox.controllers.box import BoxController
from workbox.controllers.history import HistoryController
from workbox.boxengine import BoxEngine

__all__ = ['RootController']


class RootController(BaseController):
    """The root controller for the workbox application"""

    # controllers
    box = BoxController()
    admin = AdminController(model, None, config_type=TGAdminConfig)
    error = ErrorController()
    history = HistoryController()

    def _before(self, *args, **kw):
        """Executed before running any method of Controller."""

        tmpl_context.project_name = "workbox"

    @expose('workbox.templates.index')
    def login(self, came_from=lurl('/'), failure=None, login=''):
        """ Handle login. """

        redirect('/index', params=dict(came_from=came_from))

    @expose('workbox.templates.index')
    def index(self, came_from=lurl('/'), failure=None, login=''):
        """Handle the front-page."""

        if request.identity:
            has_boxes = False
            if has_permission('manage'):
                all_boxes = BoxEngine.get_number_of_all_boxes()
                if all_boxes['created'] > 0 or all_boxes['stopped'] > 0 or all_boxes['started'] > 0:
                    has_boxes = True
            else:
                my_boxes = BoxEngine.get_number_of_user_boxes(request.identity['user']._id)
                if my_boxes['created'] > 0 or my_boxes['stopped'] > 0 or my_boxes['started'] > 0:
                    has_boxes = True

            return dict(page='index', has_boxes=has_boxes)
        else:
            error_msg = None
            if failure is not None:
                if failure == 'user-not-found':
                    error_msg = "Пользователь не найден".decode('utf8')
                elif failure == 'invalid-password':
                    error_msg = "Некорректный пароль".decode('utf8')
                else:
                    error_msg = "Ошибка авторизации".decode('utf8')

            return dict(page='index', came_from=came_from, login=login, error_msg=error_msg)

    @expose()
    def post_login(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.

        """

        if not request.identity:
            redirect('/index', params=dict(came_from=came_from))

        model.History.add_record(request.identity['repoze.who.userid'], None, "Вход в аккаунт")

        return HTTPFound(location=came_from)

    @expose()
    def post_logout(self, came_from=lurl('/')):
        """Redirect the user to the initially requested page on logout"""

        return HTTPFound(location=came_from)

    @expose()
    @require(not_anonymous(msg=l_("Only for authorized users")))
    def get_load_value(self):
        """Returns server load value."""

        if request.identity:
            return json.dumps(BoxEngine.get_server_load_value())
        else:
            return None

    @expose()
    @require(not_anonymous(msg=l_("Only for authorized users")))
    def get_number_of_user_boxes(self):
        """Returns number of all users boxes."""

        if request.identity:
            return json.dumps(BoxEngine.get_number_of_user_boxes(request.identity['user']._id))
        else:
            return None

    @expose()
    @require(not_anonymous(msg=l_("Only for authorized users")))
    def get_number_of_all_boxes(self):
        """Returns number of all boxes."""

        if request.identity:
            return json.dumps(BoxEngine.get_number_of_all_boxes())
        else:
            return None
