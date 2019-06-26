# -*- coding: utf-8 -*-
# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# Copyright 2018 Ildar Nasyrov <https://it-projects.info/team/iledarn>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import http
from openerp.http import request
from openerp.addons.website.controllers.main import Website


class WebsiteExtended(Website):

    @http.route()
    def index(self, **kw):
        website = request.website
        try:
            main_menu = request.env['website.menu'].search([
                ('website_id', '=', website.id),
                ('parent_id', '=', False)
            ], limit=1)
        except Exception:
            pass
        else:
            first_menu = main_menu.child_id and main_menu.child_id[0]
            if first_menu:
                if first_menu.url and (not (first_menu.url.startswith(('/page/', '/?', '/#')) or (first_menu.url == '/'))):
                    return request.redirect(first_menu.url)
                if first_menu.url and first_menu.url.startswith('/page/'):
                    return request.registry['ir.http'].reroute(first_menu.url)

        page = 'homepage' + str(website.id)
        full_page = 'website.' + page
        try:
            request.website.get_template(page)
        except ValueError:
            view = request.website.get_template('homepage')
            view_copy = view.sudo().copy({
                'website_id': website.id,
                'key': full_page,
            })
            request.env['ir.model.data'].sudo().create({
                'name': page,
                'model': 'ir.ui.view',
                'module': 'website',
                'res_id': view_copy.id,
            })
            # redirect to make commit
            request.redirect('/')

        return self.page(page)

    @http.route('/website_multi_company/all_websites', type='json', auth="public", website=True)
    def all_websites(self):
        current_website_id = request.website.id
        all_websites = request.env.user.backend_website_ids.filtered(lambda website: website.id != current_website_id)
        result = []
        for website in all_websites:
            result.append({'id': website.id, 'name': website.name})
        return result

    @http.route('/website_multi_company/change_website',  type='json', auth="user", website=True)
    def change_website(self, website_id, view_id):
        # TODO: open website by view
        view = request.env['ir.ui.view'].browse(view_id)
        website = request.env['website'].browse(website_id)
        request.env.user.write({
            'backend_website_id': website_id
        })
        return website.domain
