from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SogemBankAccount(models.Model):
    _name = 'sogem.bank.account'
    _description = 'Compte bancaire'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'account_number'
    _rec_name = "account_title"

    bank_id = fields.Many2one(
        "sogem.bank",
        string='Banque',
        required=True,
        tracking=True
    )

    beneficiary_id = fields.Many2one(
        'sogem.beneficiary',
        string='Titulaire de compte',
        required=True,
        tracking=True
    )

    country_id = fields.Many2one(
        'res.country',
        string='Pays',
        required=True,
        tracking=True,
        help="Pays du titulaire de compte",
        compute="_compute_country_id",
        store=True,
        readonly=False
    )
    active = fields.Boolean(default=True, tracking=True)

    account_number = fields.Char(
        string='Numéro de compte',
        required=True,
        tracking=True
    )

    account_title = fields.Char(
        string='Intitulé du compte',
        required=True,
        tracking=True,
    )

    iban = fields.Char(
        string='IBAN',
        tracking=True
    )

    bic = fields.Char(
        string='BIC/Adresse Swift',
        tracking=True
    )
    country_code = fields.Char(related='country_id.code',
        string='Code pays', tracking=True, help="Code du pays de la banque")
   
    currency_id = fields.Many2one(
        'res.currency', string='Devise', tracking=True)
    
    partner_bank_id = fields.Many2one(
        'res.partner.bank',
        string='Compte bancaire partenaire',
        readonly=True,
        tracking=True,
        help='Compte bancaire créé automatiquement dans res.partner.bank'
    )

    is_company_account = fields.Boolean(
        string='Compte de l\'entreprise',
        default=False,
        tracking=True,
        readonly=True,
        help="Cochez cette case s'il s'agit d'un compte bancaire de l'entreprise"
    )

    internal_number = fields.Char(
        string='Numéro interne',
        readonly=True,
        copy=False,
        tracking=True
    )

    active = fields.Boolean(
        default=True,
        tracking=True
    )

    _sql_constraints = [
        ('account_number_unique', 'unique(account_number)',
         'Le numéro de compte doit être unique!')
    ]
    @api.depends('account_number', 'bank_id')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.bank_id.name} - {record.account_number} "

    @api.depends('beneficiary_id')
    def _compute_country_id(self):
        for record in self:
            record.country_id = record.beneficiary_id.country_id
            record.account_title = record.beneficiary_id.name

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            # Créer automatiquement un res.partner.bank si le beneficiary a un partenaire
            if record.beneficiary_id and record.beneficiary_id.partner_id and not record.partner_bank_id:
                # Chercher ou créer la banque dans res.bank
                res_bank = False
                if record.bank_id:
                    # Chercher une banque existante par nom et pays
                    res_bank = self.env['res.bank'].search([
                        ('name', '=', record.bank_id.name),
                        ('country', '=', record.bank_id.country_id.id)
                    ], limit=1)
                    
                    # Si pas trouvée, créer une nouvelle banque
                    if not res_bank:
                        res_bank = self.env['res.bank'].create({
                            'name': record.bank_id.name,
                            'country': record.bank_id.country_id.id,
                        })
                
                # Préparer les valeurs pour res.partner.bank
                partner_bank_vals = {
                    'partner_id': record.beneficiary_id.partner_id.id,
                    'acc_number': record.account_number,
                    'acc_holder_name': record.account_title,
                }
                
                # Ajouter IBAN si disponible
                if record.iban:
                    partner_bank_vals['iban'] = record.iban
                
                # Ajouter BIC si disponible
                if record.bic:
                    partner_bank_vals['bic'] = record.bic
                
                # Ajouter la banque si disponible
                if res_bank:
                    partner_bank_vals['bank_id'] = res_bank.id
                
                # Créer le compte bancaire partenaire
                partner_bank = self.env['res.partner.bank'].create(partner_bank_vals)
                record.partner_bank_id = partner_bank.id
        
        return records
