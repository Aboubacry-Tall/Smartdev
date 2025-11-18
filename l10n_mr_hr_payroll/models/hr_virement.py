from odoo import fields, models, api


class HrBank(models.Model):
    _name = 'hr.bank'
    _description = 'Banque'

    name = fields.Char(string='Nom Banque', required=True)
    compte = fields.Char(string='Compte', required=True)

class HrVirement(models.Model):
    _name = 'hr.virement'
    _description = 'Virement'
    
    date = fields.Date(string='Date', required=True)
    bank_id = fields.Many2one('hr.bank', string='Banque', required=True)
    objet = fields.Char(string='Objet', required=True, default='Virement')
    compte = fields.Char(string='Compte', required=True)
    montant_chiffre = fields.Float(string='Montant Chiffre', required=True)
    montant_lettre = fields.Char(string='Montant lettre', required=True)

    @api.onchange('bank_id')
    def _onchange_bank_id(self):
        if self.bank_id:
            self.compte = self.bank_id.compte
