# -*- coding: utf-8 -*-
"""Sample controller with all its actions protected."""

from tg import expose, flash
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.predicates import not_anonymous

from workbox.lib.base import BaseController

__all__ = ['HistoryController']


class HistoryController(BaseController):
    """Sample controller-wide authorization"""

    # The predicate that must be met for all the actions in this controller:
    allow_only = not_anonymous(msg=l_('Only for authorized users'))

    @expose('workbox.templates.history')
    def index(self):
        return dict(page='history')
