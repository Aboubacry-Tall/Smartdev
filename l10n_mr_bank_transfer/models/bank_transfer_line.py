from odoo import models, fields, api
from odoo.tools.float_utils import float_compare


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

    exchange_rate_date = fields.Date(
        string="Date du taux utilisé",
        compute="_compute_exchange_rate_info",
        store=False,
        readonly=True,
        help="Date du taux réellement utilisé par le système (dernier taux <= date de création du virement).",
    )

    exchange_rate_date_mismatch = fields.Boolean(
        string="Décalage taux",
        compute="_compute_exchange_rate_info",
        store=False,
        readonly=True,
        help="Vrai si la date du taux réellement utilisé est différente de la date de création du virement.",
    )

    exchange_rate_used = fields.Float(
        string="Taux utilisé",
        compute="_compute_exchange_rate_info",
        store=False,
        readonly=True,
        help="Taux de conversion utilisé pour ce virement (date = date de création du virement).",
    )

    exchange_rate_latest = fields.Float(
        string="Dernier taux",
        compute="_compute_exchange_rate_info",
        store=False,
        readonly=True,
        help="Dernier taux de conversion disponible (date = aujourd'hui).",
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
        'transfer_id.create_date',
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
            # Règle: toujours utiliser le taux du jour de création du virement.
            transfer_date = (
                fields.Date.to_date(line.transfer_id.create_date)
                if line.transfer_id.create_date
                else (line.transfer_id.batch_id.date or fields.Date.context_today(line))
            )
            line.amount_converted = source_currency._convert(amount, dest_currency, company, transfer_date)

    @api.depends(
        'amount',
        'destination_currency_id',
        'transfer_id.source_currency_id',
        'transfer_id.currency_id',
        'transfer_id.create_date',
        'transfer_id.batch_id.date',
        'transfer_id.employee_id.company_id',
        'bank_account_id.currency_id',
        'bank_id.country.currency_id',
    )
    def _compute_exchange_rate_info(self):
        CurrencyRate = self.env['res.currency.rate']
        for line in self:
            company = line.transfer_id.employee_id.company_id or self.env.company
            transfer_date = (
                fields.Date.to_date(line.transfer_id.create_date)
                if line.transfer_id.create_date
                else (line.transfer_id.batch_id.date or fields.Date.context_today(line))
            )
            today = fields.Date.context_today(line)

            source_currency = line.transfer_id.source_currency_id or line.currency_id
            dest_currency = line.destination_currency_id

            def _rate_date(currency):
                if not currency:
                    return False
                rate = CurrencyRate.search(
                    [
                        ('currency_id', '=', currency.id),
                        ('name', '<=', transfer_date),
                        '|', ('company_id', '=', False), ('company_id', '=', company.id),
                    ],
                    order='name desc, id desc',
                    limit=1,
                )
                return rate.name if rate else False

            # En Odoo, la devise société n'a pas forcément de res.currency.rate ; on la considère "à la date du jour".
            company_currency = company.currency_id
            src_rate_date = transfer_date if source_currency == company_currency else _rate_date(source_currency)
            dst_rate_date = transfer_date if dest_currency == company_currency else _rate_date(dest_currency)

            # On garde une seule "date du taux" pour l'affichage : la plus récente des deux (source/destination)
            used_rate_date = max(d for d in [src_rate_date, dst_rate_date] if d) if (src_rate_date or dst_rate_date) else False
            line.exchange_rate_date = used_rate_date

            # Alerte demandée: comparer le "dernier taux" réellement utilisé par le virement (date <= virement)
            # à la date de création du virement. Si le taux date d'hier, on doit alerter.
            if not source_currency or not dest_currency or source_currency == dest_currency:
                line.exchange_rate_used = 1.0
                line.exchange_rate_latest = 1.0
                line.exchange_rate_date_mismatch = False
                continue

            used_rate = source_currency._get_conversion_rate(source_currency, dest_currency, company, transfer_date)
            latest_rate = source_currency._get_conversion_rate(source_currency, dest_currency, company, today)

            line.exchange_rate_used = used_rate
            line.exchange_rate_latest = latest_rate

            # mismatch si la date du taux réellement utilisé n'est pas celle du virement
            # (ou si un taux manque -> _rate_date False)
            line.exchange_rate_date_mismatch = bool(
                (src_rate_date and src_rate_date != transfer_date) or
                (dst_rate_date and dst_rate_date != transfer_date) or
                (not src_rate_date and source_currency != company_currency) or
                (not dst_rate_date and dest_currency != company_currency)
            )
    
    @api.onchange('transfer_id')
    def _onchange_transfer_id(self):
        """Par défaut, suggérer le montant du salaire"""
        if self.transfer_id and self.transfer_id.salaire:
            self.amount = self.transfer_id.salaire

