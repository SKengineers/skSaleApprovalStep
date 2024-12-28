# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from ast import literal_eval
from datetime import datetime, date, timedelta


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sale_approval_ids = fields.Many2many('res.users', string='Sale Approvers')
    approval_line_ids = fields.One2many('approval.line', 'order_id')
    reason_reject = fields.Text(string='Reason Reject')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Quotation Sent'),
        ('waiting_approval', 'Waiting For Approval'),
        ('approved', 'Approved'),
        ('sale', 'Sales Order'),
        ('rejected', 'Rejected'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, default='draft', tracking=True)
    current_user = fields.Boolean(string='Check current User', compute='compute_current_user')

    def action_draft(self):
        orders = self.filtered(lambda s: s.state in ['cancel', 'sent', 'rejected'])
        return orders.write({
            'state': 'draft',
            'signature': False,
            'signed_by': False,
            'signed_on': False,
        })

    def compute_current_user(self):
        for rec in self:
            user_id = self.env['res.users'].browse(self.env.user.id)
            if user_id:
                if user_id.id not in rec.sale_approval_ids.ids:
                    rec.current_user = False
                else:
                    rec.current_user = True
            else:
                rec.current_user = False

    def send_so_for_approval(self):
        for rec in self:
            user_config = self.env['ir.config_parameter'].get_param('ag_sale_approval_step.sale_user_approve_ids')
            user_ids = self.env['res.users'].search([
                ('id', 'in', literal_eval(user_config))
            ])
            rec.sale_approval_ids = [(6, 0, user_ids.ids)]
            for user in user_ids:
                self.env['approval.line'].create({
                    'order_id': rec.id,
                    'user_id': user.id
                })
                self.env['mail.activity'].create({
                    'activity_type_id': self.env.ref('mail.mail_activity_data_email').id,
                    'summary': "Approve Sale Order",
                    'note': 'Sale %s is send for approval, for customer %s, please approve' % (rec.name, rec.partner_id.name),
                    'res_id': rec.id,
                    'date_deadline': datetime.today(),
                    'res_model_id': self.env.ref('sale.model_sale_order').id,
                    'user_id': user.id
                })
            rec.state = 'waiting_approval'

    def action_approve(self):
        for rec in self:
            for user in rec.approval_line_ids.filtered(lambda x: x.user_id.id == self.env.user.id):
                rec.message_post(body='Order is Approved by %s' % self.env.user.name, subject="Approve Order")
                user.approved = True
            if not any(rec.approval_line_ids.filtered(lambda x: not x.approved)):
                rec.state = 'approved'

    def action_reject(self):
        return self.env.ref('ag_sale_approval_step.sale_order_reject_reason_action').read()[0]