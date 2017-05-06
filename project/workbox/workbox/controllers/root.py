# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, lurl
from tg import request, redirect, tmpl_context
from tg.exceptions import HTTPFound
from tg.predicates import has_permission
from tgext.admin.mongo import BootstrapTGMongoAdminConfig as TGAdminConfig
from tgext.admin.controller import AdminController

from workbox import model
from workbox.lib.base import BaseController
from workbox.controllers.error import ErrorController
from workbox.controllers.box import BoxController
from workbox.boxengine import BoxEngine


__all__ = ['RootController']


class RootController(BaseController):
    """The root controller for the workbox application"""

    #controllers
    box = BoxController()
    admin = AdminController(model, None, config_type=TGAdminConfig)
    error = ErrorController()

    def _before(self, *args, **kw):
        """Executed before running any method of Controller"""

        tmpl_context.project_name = "workbox"

    @expose('workbox.templates.index')
    def index(self):
        """Handle the front-page"""

        if request.identity:
            load_value = BoxEngine.get_server_load_value()
            my_boxes = BoxEngine.get_number_of_user_boxes(request.identity['user']._id)
            all_boxes = BoxEngine.get_number_of_all_boxes()

            boxes = model.Box.get_all_user_boxes(request.identity['user']._id)
            boxes = sorted(boxes, key=lambda x: x.datetime_of_modify, reverse=True)

            return dict(page='index', load_value=load_value, my_boxes=my_boxes,
                        all_boxes=all_boxes, last_ten_worked=boxes[:10])
        else:
            return dict(page='index')

    @expose('workbox.templates.history')
    def history(self):
        """Handle the history page"""

        entries = None

        if has_permission('manage'):
            entries = model.History.get_all_records()
        else:
            entries = model.History.get_all_user_records(request.identity['user']._id)

        return dict(page='history', entries=entries)

    @expose('workbox.templates.login')
    def login(self, came_from=lurl('/'), failure=None, login=''):
        """Start the user login"""

        if request.identity:
            return HTTPFound(location='/')

        error_msg = None
        if failure is not None:
            if failure == 'user-not-found':
                error_msg = 'Пользователь не найден'.decode("utf8")
            elif failure == 'invalid-password':
                error_msg = 'Некорректный пароль'.decode("utf8")
            else:
                error_msg = 'Ошибка авторизации'.decode("utf8")

        return dict(page='login', came_from=came_from, login=login, error_msg=error_msg)

    @expose()
    def post_login(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed

        """

        if not request.identity:
            redirect('/login', params=dict(came_from=came_from))

        model.History.add_record(request.identity['repoze.who.userid'], None, 'Вход в аккаунт')

        return HTTPFound(location=came_from)

    @expose()
    def post_logout(self, came_from=lurl('/')):
        """Redirect the user to the initially requested page on logout"""

        return HTTPFound(location=came_from)
