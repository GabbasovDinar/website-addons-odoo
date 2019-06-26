# -*- coding: utf-8 -*-
from openerp import models


class QWeb(models.AbstractModel):
    _inherit = 'ir.qweb'

    def render(self, cr, uid, id_or_xml_id, qwebcontext=None, loader=None, context=None):
        if context is None:
            context = {}
        website_id = context.get('website_id')
        if website_id:
            if isinstance(id_or_xml_id, (int, long)):
                id_or_xml_id = self.pool["ir.ui.view"].browse(cr, uid, id_or_xml_id, context=context).key

            domain = [('key', '=', id_or_xml_id), '|', ('website_id', '=', website_id), ('website_id', '=', False)]
            version_id = context.get('version_id')
            domain += version_id and ['|', ('version_id', '=', False), ('version_id', '=', version_id)] or [('version_id', '=', False)]

            version_specific_view = self.pool["ir.ui.view"].search(cr, uid, domain, order='website_id, version_id', limit=1, context=context)
            if version_specific_view:
                id_or_xml_id = version_specific_view[0]

        return super(QWeb, self).render(cr, uid, id_or_xml_id, qwebcontext, loader=loader, context=context)
