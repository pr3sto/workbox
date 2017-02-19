# -*- coding: utf-8 -*-
"""Boxes actions controller."""

from tg import expose
from tg.i18n import lazy_ugettext as l_
from tg.predicates import not_anonymous

from workbox.lib.base import BaseController

__all__ = ['HistoryController']


class HistoryController(BaseController):
    """History actions controller"""

    # The predicate that must be met for all the actions in this controller:
    allow_only = not_anonymous(msg=l_('Only for authorized users'))

    @expose('workbox.templates.history')
    def index(self):
        return dict(page='history')
