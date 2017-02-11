# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, lurl
from tg import request, redirect, tmpl_context
from tg.exceptions import HTTPFound
from project import model
from tgext.admin.mongo import BootstrapTGMongoAdminConfig as TGAdminConfig
from tgext.admin.controller import AdminController

from project.lib.base import BaseController
from project.controllers.error import ErrorController
from project.controllers.container import ContainerController
from project.controllers.history import HistoryController


__all__ = ['RootController']


class RootController(BaseController):
    """The root controller for the Project application"""

    container = ContainerController()
    history = HistoryController()
    admin = AdminController(model, None, config_type=TGAdminConfig)
    error = ErrorController()

    def _before(self, *args, **kw):
        tmpl_context.project_name = "project"

    @expose('project.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict(page='index')

    @expose('project.templates.login')
    def login(self, came_from=lurl('/'), failure=None, login=''):
        """Start the user login."""
        error_msg = None
        if failure is not None:
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
