# -*- coding: utf-8 -*-
from openerp import models, fields, api
import openerp


class Website(models.Model):
    _inherit = "website"

    @api.model
    def publish_page(self, view_id, value):
        view = self.env['ir.ui.view'].browse(view_id)
        if view:
            view.write({
                'is_publish': bool(value)
            })

    def new_page(self, cr, uid, name, template='website.default_page', ispage=True, context=None):
        page_xmlid = super(Website, self).new_page(cr, uid, name, template, ispage, context)
        context = context or {}
        view_obj = self.pool.get('ir.ui.view')
        dom = [('website_id', '=', False), ('website_id', '=', context.get('website_id'))]
        page_ids = view_obj.search(cr, openerp.SUPERUSER_ID, [('key', '=', page_xmlid), '|'] + dom, context=dict(context or {}, active_test=False))
        view_obj.write(cr, openerp.SUPERUSER_ID, page_ids, {'is_publish': False}, context=context)
        return page_xmlid
