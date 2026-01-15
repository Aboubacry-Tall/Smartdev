# -*- coding: utf-8 -*-

from odoo import models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    def create_invoices(self):
        """Bloquer la création de factures pour les techniciens"""
        group_technicien = self.env.ref('wg_management.group_technicien', raise_if_not_found=False)
        if group_technicien and self.env.user.id in group_technicien.user_ids.ids:
            raise UserError(_("Les techniciens ne sont pas autorisés à créer des factures."))
        return super().create_invoices()

