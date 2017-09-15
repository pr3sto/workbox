# -*- coding: utf-8 -*-
"""History actions controller."""

import json

from tg import request
from tg import expose
from tg.i18n import lazy_ugettext as l_
from tg.predicates import not_anonymous, has_permission

from workbox import model
from workbox.lib.base import BaseController

__all__ = ['HistoryController']


class HistoryController(BaseController):
    """History actions controller"""

    # The predicate that must be met for all the actions in this controller:
    allow_only = not_anonymous(msg=l_('Only for authorized users'))

    @expose('workbox.templates.history')
    def index(self):
        """Handle the history page."""

        return dict(page='history')

    @expose()
    def get(self):
        """Returns history data."""

        entries = None
        data = []

        if has_permission('manage'):
            entries = model.History.get_all_records()

            for entry in entries:
                box = []
                box.append(entry.history_id)
                box.append(entry.user.display_name)
                if entry.box:
                    box.append(entry.box.box_id)
                else:
                    box.append(' - ')
                box.append(entry.datetime.strftime("%Y-%m-%d %H:%M"))
                box.append(entry.info)
                data.append(box)
        else:
            entries = model.History.get_all_user_records(request.identity['user']._id)

            for entry in entries:
                box = []
                box.append(entry.history_id)
                if entry.box:
                    box.append(entry.box.box_id)
                else:
                    box.append(' - ')
                box.append(entry.datetime.strftime("%Y-%m-%d %H:%M"))
                box.append(entry.info)
                data.append(box)

        json_entries = {}
        json_entries['data'] = data
        return json.dumps(json_entries)
