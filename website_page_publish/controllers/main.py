# -*- coding: utf-8 -*-
from openerp.addons.web import http
from openerp.http import request
from openerp.addons.website.controllers.main import Website


class NewWebsite(Website):
    @http.route('/page/<page:page>', type='http', auth="public", website=True, cache=300)
    def page(self, page, **opt):
        res = super(NewWebsite, self).page(page, **opt)
        values = {
            'path': page,
            'deletable': True
        }
        if page.startswith('website.'):
            url = '/page/' + page[8:]
            if request.httprequest.query_string:
                url += '?' + request.httprequest.query_string
            return request.redirect(url, code=301)
        elif '.' not in page:
            page = 'website.%s' % page
        try:
            view = request.website.get_template(page)
            if not view.is_publish:
                if not request.env.user.has_group('base.group_website_publisher'):
                    return request.render('website.page_404', values)
        except ValueError, e:
            pass

        return res
