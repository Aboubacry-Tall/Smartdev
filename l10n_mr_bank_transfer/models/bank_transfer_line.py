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

    destination_currency_id = fields.Many2one(
        'res.currency',
        string='Devise destination',
        compute='_compute_destination_currency_id',
        store=True,
        readonly=True,
    )

    amount_converted = fields.Monetary(
        string='Montant converti',
        currency_field='destination_currency_id',
        compute='_compute_amount_converted',
        store=True,
        readonly=True,
        help="Montant converti de la devise source vers la devise de la banque de destination selon le taux du jour.",
    )
    
    # Informations supplémentaires
    notes = fields.Text(string='Notes')

    @api.depends(
        'bank_account_id',
        'bank_account_id.currency_id',
        'bank_id',
        'bank_id.country',
        'bank_id.country.currency_id',
        'transfer_id.currency_id',
    )
    def _compute_destination_currency_id(self):
        for line in self:
            # Devise de destination :
            # 1) devise du compte bancaire (si renseignée)
            # 2) sinon devise du pays de la banque
            # 3) sinon devise du virement (lot)
            dest = line.bank_account_id.currency_id if line.bank_account_id else False
            if not dest and line.bank_id and line.bank_id.country:
                dest = line.bank_id.country.currency_id
            line.destination_currency_id = dest or line.transfer_id.currency_id

    @api.depends(
        'amount',
        'destination_currency_id',
        'transfer_id.source_currency_id',
        'transfer_id.batch_id.date',
        'transfer_id.employee_id.company_id',
    )
    def _compute_amount_converted(self):
        for line in self:
            # La saisie du montant se fait dans la devise "source" (lot).
            # Par sécurité, si elle n'est pas disponible, utiliser la devise du montant.
            source_currency = line.transfer_id.source_currency_id or line.currency_id
            dest_currency = line.destination_currency_id
            amount = line.amount or 0.0

            if not source_currency or not dest_currency:
                line.amount_converted = 0.0
                continue

            if source_currency == dest_currency:
                line.amount_converted = amount
                continue

            company = line.transfer_id.employee_id.company_id or self.env.company
            date = line.transfer_id.batch_id.date or fields.Date.context_today(line)
            line.amount_converted = source_currency._convert(amount, dest_currency, company, date)
    
    @api.onchange('transfer_id')
    def _onchange_transfer_id(self):
        """Par défaut, suggérer le montant du salaire"""
        if self.transfer_id and self.transfer_id.salaire:
            self.amount = self.transfer_id.salaire

