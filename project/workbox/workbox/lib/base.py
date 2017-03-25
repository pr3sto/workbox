# -*- coding: utf-8 -*-
"""The base Controller API"""

from tg import TGController, tmpl_context
from tg import request

__all__ = ['BaseController']


class BaseController(TGController):
    """
    Base class for the controllers in the application

    Your web application should have one of these. The root of
    your application is used to compute URLs used by your app

    """

    def __call__(self, environ, context):
        """Invoke the Controller"""

        tmpl_context.identity = request.identity

        return TGController.__call__(self, environ, context)
