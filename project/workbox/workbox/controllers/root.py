# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, lurl
from tg import request, redirect, tmpl_context
from tg.exceptions import HTTPFound
from workbox import model
from tgext.admin.mongo import BootstrapTGMongoAdminConfig as TGAdminConfig
from tgext.admin.controller import AdminController

from workbox.lib.base import BaseController
from workbox.controllers.error import ErrorController
from workbox.controllers.box import BoxController
from workbox.controllers.history import HistoryController


__all__ = ['RootController']


class RootController(BaseController):
    """The root controller for the workbox application"""

    box = BoxController()
    history = HistoryController()
    admin = AdminController(model, None, config_type=TGAdminConfig)
    error = ErrorController()

    def _before(self, *args, **kw):
        tmpl_context.project_name = "workbox"

    @expose('workbox.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict(page='index')

    @expose('workbox.templates.help')
    def help(self):
        """Handle the help-page."""
        return dict(page='help')

    @expose('workbox.templates.login')
    def login(self, came_from=lurl('/'), failure=None, login=''):
        if request.identity:
            return HTTPFound(location='/')

        """Start the user login."""
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
        authentication or redirect her back to the login page if login failed.

        """
        if not request.identity:
            redirect('/login', params=dict(came_from=came_from))

        return HTTPFound(location=came_from)

    @expose()
    def post_logout(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on logout.

        """
        return HTTPFound(location=came_from)
