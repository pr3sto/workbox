# -*- coding: utf-8 -*-
"""Error controller"""

from tg import request, expose
from workbox.lib.base import BaseController

__all__ = ['ErrorController']


class ErrorController(BaseController):
    """
    Generates error documents as and when they are required.

    The ErrorDocuments middleware forwards to ErrorController when error
    related status codes are returned from the application.

    This behaviour can be altered by changing the parameters to the
    ErrorDocuments middleware in your config/middleware.py file.

    """

    @expose('workbox.templates.error')
    def document(self, *args, **kwargs):
        """Render the error document."""

        resp = request.environ.get('tg.original_response')
        resp_code = request.params.get('code', resp.status_int)
        try:
            # tg.abort exposes the message as .detail in response
            message = resp.detail
        except:
            message = None

        if not message:
            if resp_code == 403:
                message = "У Вас нет прав доступа для просмотра этой страницы"
            elif resp_code == 404:
                message = "Запрашиваемая страница не найдена"
            elif resp_code == 500:
                message = "Внутренняя ошибка сервера"
            # add more codes
            else:
                message = "Извините, мы не может обработать запрос"

        values = dict(prefix=request.environ.get('SCRIPT_NAME', ''),
                      code=resp_code,
                      message=request.params.get('message', message.decode('utf8')))
        return values
