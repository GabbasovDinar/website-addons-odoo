# -*- coding: utf-8 -*-
from lxml import etree
from openerp import tools, fields, models, api


class View(models.Model):

    _inherit = "ir.ui.view"

    version_id = fields.Many2one('website_version.version', ondelete='cascade', string="Version")

    def _sort_suitability_key(self):
        original_suitability = super(View, self)._sort_suitability_key()
        context_version_id = self.env.context.get('version_id', 0)
        different_version = context_version_id != (self.version_id.id or 0)
        return (different_version, original_suitability)

    @api.multi
    def write(self, vals):
        if self.env.context is None:
            self.env.context = {}
        version_id = self.env.context.get('version_id')
        if version_id and not self.env.context.get('write_on_view') and not 'active' in vals:
            self.env.context = dict(self.env.context, write_on_view=True)
            version = self.env['website_version.version'].browse(version_id)
            website_id = version.website_id.id
            version_view_ids = self.env['ir.ui.view']
            for current in self:
                if current.version_id.id == version_id:
                    version_view_ids += current
                else:
                    new_v = self.search([('website_id', '=', website_id), ('version_id', '=', version_id), ('key', '=', current.key)])
                    if new_v:
                        version_view_ids += new_v
                    else:
                        copy_v = current.copy({'version_id': version_id, 'website_id': website_id})
                        version_view_ids += copy_v
            return super(View, version_view_ids).write(vals)
        else:
            self.env.context = dict(self.env.context, write_on_view=True)
            return super(View, self).write(vals)

    @api.one
    def publish(self):
        master_record = self.search([('key', '=', self.key), ('version_id', '=', False), ('website_id', '=', self.website_id.id)])
        if master_record:
            master_record.unlink()
        self.copy({'version_id': None})

    @api.multi
    def action_publish(self):
        self.publish()

    @api.model
    def get_view_id(self, xml_id):
        if self.env.context and 'website_id' in self.env.context and not isinstance(xml_id, (int, long)):
            domain = [('key', '=', xml_id), '|', ('website_id', '=', self.env.context['website_id']), ('website_id', '=', False)]
            if 'version_id' in self.env.context:
                domain += ['|', ('version_id', '=', self.env.context['version_id']), ('version_id', '=', False)]
            v = self.search(domain, order='website_id,version_id', limit=1)
            if v:
                return v.id
        return super(View, self).get_view_id(xml_id)

    @tools.ormcache_context('uid', 'view_id',
        keys=('lang', 'inherit_branding', 'editable', 'translatable', 'edit_translations', 'website_id', 'version_id'))
    def _read_template(self, cr, uid, view_id, context=None):
        arch = self.read_combined(cr, uid, view_id, fields=['arch'], context=context)['arch']
        arch_tree = etree.fromstring(arch)
        self.distribute_branding(arch_tree)
        root = etree.Element('templates')
        root.append(arch_tree)
        arch = etree.tostring(root, encoding='utf-8', xml_declaration=True)
        return arch

    @api.model
    def get_inheriting_views_arch(self, view_id, model):
        arch = super(View, self).get_inheriting_views_arch(view_id, model)
        vw = self.browse(view_id)
        if not (self.env.context and self.env.context.get('website_id') and vw.type == 'qweb'):
            return arch

        # keep the most suited view when several view with same key are available
        chosen_view_ids = self.browse(view_id for _, view_id in arch).filter_duplicate().ids

        return [x for x in arch if x[1] in chosen_view_ids]

    def toggle(self, cr, uid, ids, context=None):
        """ Switches between enabled and disabled statuses
        """
        for view in self.browse(cr, uid, ids, context=dict(context or {}, active_test=False)):
            all_id = self.search(cr, uid, [('key', '=', view.key)], context=dict(context or {}, active_test=False))
            for v in self.browse(cr, uid, all_id, context=dict(context or {}, active_test=False)):
                v.write({'active': not v.active})

    @api.model
    def customize_template_get(self, key, full=False, bundles=False, **kw):
        result = super(View, self).customize_template_get(key, full=full, bundles=bundles, **kw)
        check = []
        res = []
        for data in result:
            if data['name'] not in check:
                check.append(data['name'])
                res.append(data)
        return res
