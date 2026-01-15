# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    create_contract = fields.Boolean(string='Créer un contrat', default=False, 
                                     help='Si coché, un contrat sera créé automatiquement lors de la confirmation de la facture')
    
    def action_post(self):
        """Surcharger action_post pour créer un contrat si demandé"""
        result = super().action_post()
        
        # Créer un contrat pour chaque facture qui a le champ create_contract coché
        for move in self:
            if move.create_contract and move.move_type in ('out_invoice', 'out_refund'):
                # Définir le type de contact à 'C' (Client) pour que le partenaire apparaisse dans la liste des clients
                if move.partner_id:
                    move.partner_id.write({'type_contact': 'C'})
                move._create_contract_from_invoice()
        
        return result
    
    def _create_contract_from_invoice(self):
        """Créer un contrat à partir de la facture"""
        self.ensure_one()
        
        if not self.partner_id:
            raise UserError("Impossible de créer un contrat : le client n'est pas défini sur la facture.")
        
        # Récupérer le premier produit des lignes de facture
        product_line = self.invoice_line_ids.filtered(lambda l: l.product_id and l.product_id.sale_ok)
        if not product_line:
            raise UserError("Impossible de créer un contrat : aucun produit vendable trouvé dans les lignes de facture.")
        
        # Prendre le premier produit
        product = product_line[0].product_id
        
        # Calculer la durée en mois (par défaut 1 mois, ou basé sur la quantité si applicable)
        duration_months = 1
        if product_line[0].quantity and product_line[0].quantity > 0:
            # Si la quantité représente des mois, l'utiliser
            duration_months = int(product_line[0].quantity)
        
        # Date de début : utiliser la date de la facture ou aujourd'hui
        start_date = self.invoice_date or fields.Date.today()
        
        # Créer le contrat
        contract_vals = {
            'partner_id': self.partner_id.id,
            'invoice_id': self.id,
            'product_id': product.id,
            'start_date': start_date,
            'duration_months': duration_months,
            'currency_id': self.currency_id.id,
            'state': 'draft',
        }
        
        contract = self.env['wg.contract'].create(contract_vals)
        
        # Lier la facture au contrat
        contract.write({'invoice_ids': [(4, self.id)]})
        
        return contract

