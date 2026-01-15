# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    reference = fields.Char(string='Reference')
    note = fields.Text(string='Note')
    image = fields.Binary(string='Image')
    sale_order_id = fields.Many2one('sale.order', string='Devis')

    
    def action_create_payments(self):
        # Récupérer le devis depuis la facture
        invoice = self.env['account.move'].search([('name', '=', self.communication)], limit=1)
        if invoice:
            # Chercher le devis lié à la facture via les lignes de facture
            sale_order = invoice.invoice_line_ids.mapped('sale_line_ids.order_id')
            if sale_order:
                self.write({
                    'sale_order_id': sale_order[0].id,
                })
        return super().action_create_payments()

