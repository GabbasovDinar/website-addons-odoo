# -*- coding: utf-8 -*-

from openerp.addons.web.controllers.main import Session
from openerp.http import request


class Session(Session):

    def session_info(self):
        res = super(Session, self).session_info()
        user = request.env.user
        display_switch_website_menu = user.has_group('web_website.group_multi_website') and len(user.backend_website_ids) > 1
        res['user_websites'] = {
            'current_website': (
                user.backend_website_id.id,
                user.backend_website_id.name
            ) if user.backend_website_id else False,
            'allowed_websites': [
                (w.id, w.name)
                for w in user.backend_website_ids
            ]
        } if display_switch_website_menu else False

        return res
