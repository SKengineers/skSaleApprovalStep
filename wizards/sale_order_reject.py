# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError
from datetime import datetime


class SaleOrderRejectReason(models.TransientModel):
    _name = 'sale.order.reject.reason'
    _description = "Sale Order Reject Reason"

    reason_reject = fields.Text(string='Reason')

    def action_confirm(self):
        active_id = self.env.context.get('active_id')
        sale_order = self.env['sale.order'].browse(active_id)
        approve_line_id = sale_order.approval_line_ids.filtered(lambda x: x.user_id.id == self.env.user.id)
        if approve_line_id:
            approve_line_id.reason_reject = self.reason_reject
        sale_order.state = 'rejected'







