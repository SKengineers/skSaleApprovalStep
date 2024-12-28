# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from ast import literal_eval


class ApprovalLine(models.Model):
    _name = 'approval.line'

    user_id = fields.Many2one('res.users', string='Sale Approvers')
    approved = fields.Boolean(string='Approved', default=False)
    reason_reject = fields.Text(string='Reject Reason')
    order_id = fields.Many2one('sale.order')