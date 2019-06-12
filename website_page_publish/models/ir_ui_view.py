# -*- coding: utf-8 -*-
from openerp import models, fields, api, _


class View(models.Model):
    _inherit = "ir.ui.view"

    is_publish = fields.Boolean(default=True)
