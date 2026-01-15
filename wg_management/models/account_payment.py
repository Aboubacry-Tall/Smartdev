# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AccountPayment(models.Model):
    _inherit = "account.payment"

    payment_register_id = fields.Integer(string="Payment Register ID")
    sale_order_id = fields.Many2one('sale.order', string='Devis')
    reference = fields.Char(string='Reference')
    image = fields.Binary(string='Image')
    note = fields.Text(string='Note')

    @api.model_create_multi
    def create(self, vals_list):
        
        for vals in vals_list:
            if vals.get('memo'):
                payment_register = self.env['account.payment.register'].search([('communication', '=', vals['memo'])], limit=1)
                if payment_register:
                    vals['payment_register_id'] = payment_register.id
                    if hasattr(payment_register, 'sale_order_id') and payment_register.sale_order_id:
                        vals['sale_order_id'] = payment_register.sale_order_id.id
                    if hasattr(payment_register, 'reference') and payment_register.reference:
                        vals['reference'] = payment_register.reference
                    if hasattr(payment_register, 'image') and payment_register.image:
                        vals['image'] = payment_register.image
                    if hasattr(payment_register, 'note') and payment_register.note:
                        vals['note'] = payment_register.note
                else:
                    raise UserError("La référence n'est pas associée à un paiement.")
            else:
                raise UserError("La référence est requise.")
        return super().create(vals_list)

