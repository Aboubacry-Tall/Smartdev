from odoo import models, fields, api


class BankTransferLine(models.Model):
    """Ligne de virement par compte bancaire"""
    _name = 'bank.transfer.line'
    _description = 'Ligne de virement par compte bancaire'
    _order = 'sequence, id'

    sequence = fields.Integer(string='Séquence', default=10)
    
    transfer_id = fields.Many2one(
        'bank.transfer',
        string='Virement',
        required=True,
        ondelete='cascade',
        index=True
    )
    
    bank_account_id = fields.Many2one(
        'res.partner.bank',
        string='Compte bancaire',
        required=True,
        ondelete='restrict'
    )
    
    # Champs related du compte bancaire
    bank_id = fields.Many2one(
        'res.bank',
        string='Banque',
        related='bank_account_id.bank_id',
        readonly=True,
        store=True
    )
    
    acc_number = fields.Char(
        string='Numéro de compte',
        related='bank_account_id.acc_number',
        readonly=True
    )
    
    bank_bic = fields.Char(
        string='Code BIC',
        related='bank_account_id.bank_bic',
        readonly=True
    )
    
    # Montant à virer sur ce compte
    amount = fields.Monetary(
        string='Montant à virer',
        currency_field='currency_id',
        required=True,
        help='Montant qui sera viré sur ce compte bancaire'
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Devise',
        related='transfer_id.currency_id',
        readonly=True
    )
    
    # Informations supplémentaires
    notes = fields.Text(string='Notes')
    
    @api.onchange('transfer_id')
    def _onchange_transfer_id(self):
        """Par défaut, suggérer le montant du salaire"""
        if self.transfer_id and self.transfer_id.salaire:
            self.amount = self.transfer_id.salaire

