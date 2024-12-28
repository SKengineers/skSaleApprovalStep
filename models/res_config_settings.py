# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from ast import literal_eval


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sale_user_approve_ids = fields.Many2many('res.users', string='Sale Approvers')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        sale_approve_ids = self.env['ir.config_parameter'].sudo()
        approvers_ids = sale_approve_ids.get_param('ag_sale_approval_step.sale_user_approve_ids')
        res.update(
            sale_user_approve_ids=[(6, 0, literal_eval(approvers_ids))]
        )
        return res

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('ag_sale_approval_step.sale_user_approve_ids', self.sale_user_approve_ids.ids)
        return res