from io import BytesIO
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from num2words import num2words
import qrcode
import base64
import logging
_logger = logging.getLogger(__name__)


class Transfer(models.Model):
    _name = 'sogem.transfer'
    _description = 'Virement'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'

    name = fields.Char(string='Référence', readonly=True,
                       default=lambda self: _('Nouveau'))
    date = fields.Date(string='Date', required=True,
                       default=fields.Date.context_today, tracking=True)
    source_account_id = fields.Many2one(
        'sogem.bank.account', string='Compte source', required=True, tracking=True,
        domain=[('is_company_account', '=', True)],
        help="Le compte source doit être un compte bancaire de l'entreprise")
    destination_account_id_account_id = fields.Many2one(
        'sogem.bank.account', string='Compte de destination', tracking=True)

    destination_account_id_account_number = fields.Char(
        related='destination_account_id_account_id.account_number')

    amount = fields.Monetary(string='Montant')

    description = fields.Text(string='Description')

    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('confirmed', 'Confirmé'),
        ('done', 'Effectué'),
        ('cancelled', 'Annulé')
    ], string='Statut', default='draft', tracking=True)
    transfer_type = fields.Selection([
        ('simple', 'Virement Simple'),
        ('multiple', 'Virement Multiple'),
        ('interbank', 'Virement Interbancaire'),
        ('transfer', 'Transfert'),
    ], string='Type de virement', required=True,  tracking=True)
    destination_account_id = fields.Many2one(
        'sogem.bank.account', string='Compte destination')

    beneficiary_id = fields.Many2one(
        'sogem.beneficiary', string='Bénéficiaire')

    beneficiary_address = fields.Char(
        related="beneficiary_id.address", string="Adresse du Bénéficiaire")
    # beneficiary_bank = fields.Many2one(
    #     related="beneficiary_id.bank_id", string="Banque du Bénéficiaire")
    # iban = fields.Char(related="beneficiary_id.iban", string="IBAN")
    # bic = fields.Char(
    #     related="beneficiary_id.bic", string="BIC / Swift")

    currency_id = fields.Many2one(related="source_account_id.currency_id", string='Devise',
                                  )

    transfer_line_ids = fields.One2many(
        'sogem.transfer.line', 'transfer_id', string='Lignes de virement')

    amount_total = fields.Monetary(
        string='Montant total', compute='_compute_total_amount', store=True)
    amount_text = fields.Char(
        string='Montant en lettres', compute='_compute_amount_text', store=True)

    transfer_subtype = fields.Selection([
        ('salaire', 'Salaire (Personnel)'),
        ('prime', 'Primes Communautaires (Administrateurs)'),
        ('prestataire', 'Prestataires (Consultants)'),
    ], string='Sous-type de virement', tracking=True)
    

    @api.depends('transfer_line_ids.amount')
    def _compute_total_amount(self):
        for record in self:
            record.amount_total = sum(
                record.transfer_line_ids.mapped('amount'))

    def amount_to_letters(self, amount):
        return num2words(amount, lang='fr').upper() + ' ' + record.currency_id.name if amount else ''

    @api.depends('amount_total')
    def _compute_amount_text(self):
        for record in self:
            record.amount_text = num2words(record.amount_total, lang='fr').upper(
            ) + ' ' + record.currency_id.name if record.amount_total else ''

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('Nouveau')) == _('Nouveau'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sogem.transfer') or _('Nouveau')
        return super().create(vals_list)

    def action_confirm(self):
        self.ensure_one()
        if not self.transfer_line_ids:
            raise ValidationError(
                _('Veuillez ajouter au moins un bénéficiaire avec un montant.'))
        if any(line.amount <= 0 for line in self.transfer_line_ids):
            raise ValidationError(
                _('Le montant de chaque ligne doit être supérieur à zéro.'))
        self.state = 'confirmed'

    def action_done(self):
        self.ensure_one()
        if self.state != 'confirmed':
            raise ValidationError(
                _('Le virement doit être confirmé avant d\'être effectué'))
        self.state = 'done'

    def action_cancel(self):
        self.ensure_one()
        if self.state == 'done':
            raise ValidationError(
                _('Un virement effectué ne peut pas être annulé'))
        self.state = 'cancelled'

    def action_draft(self):
        self.ensure_one()
        self.state = 'draft'

    def get_qr_code(self):
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(self.name or '')
        qr.make(fit=True)
        img = qr.make_image()
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        return base64.b64encode(buffer.getvalue()).decode()

    def get_lines_by_bank(self):
        grouped = {}
        for line in self.transfer_line_ids:
            bank = line.account_id.bank_id
            grouped.setdefault(bank, []).append(line)
        return grouped

    def get_amount_text(self, bank_id):
        bank_total = sum(
            self.transfer_line_ids.filtered(lambda l: l.beneficiary_id.bank_id.id == bank_id).mapped('amount'))
        return self.currency_id.amount_to_text(bank_total)

    def action_print_summary(self):
        self.ensure_one()
        return self.env.ref('odoo_virements.action_report_transfer_summary').report_action(self)

    def action_print_bank_details(self):
        self.ensure_one()
        return self.env.ref('odoo_virements.action_report_transfer_bank_details').report_action(self)

    def action_print_simple(self):
        self.ensure_one()
        return self.env.ref('odoo_virements.action_report_transfer').report_action(self)


class TransferLine(models.Model):
    _name = 'sogem.transfer.line'
    _description = 'Ligne de virement'
    _order = 'sequence, id'

    sequence = fields.Integer(default=10)
    transfer_id = fields.Many2one(
        'sogem.transfer', required=True, ondelete='cascade')
    currency_id = fields.Many2one(
        'res.currency', related='transfer_id.currency_id', store=True, readonly=True)
    beneficiary_id = fields.Many2one(
        'sogem.beneficiary', string='Bénéficiaire', required=True)

    description = fields.Text(string='Motif')

    account_id = fields.Many2one('sogem.bank.account', string="Compte bancaire",
                                 required=True, domain="[('beneficiary_id', '=', beneficiary_id)]")
    amount = fields.Monetary(required=True)
    amount_text = fields.Char(string="Montant en texte", compute="_compute_amount_text")

    @api.depends('amount')
    def _compute_amount_text(self):
        for rec in self:
            if rec.amount is not None:
                # Format: Séparateur de milliers, sans décimales (ex: "1 234 567")
                rec.amount_text = '{:,.0f}'.format(rec.amount).replace(',', ' ').replace('.', ' ')
            else:
                rec.amount_text = '0'




    