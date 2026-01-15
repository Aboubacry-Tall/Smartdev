from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SogemBank(models.Model):
    _name = 'sogem.bank'
    _description = 'Banque'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Nom de la banque', required=True, tracking=True)
    country_id = fields.Many2one(
        'res.country', string='Pays', required=True, tracking=True, help="Sélectionnez le pays où la banque est située.")
    country_code = fields.Char(
        string='Code pays', tracking=True, help="Code du pays de la banque")
   
    currency_id = fields.Many2one(
        'res.currency', string='Devise', tracking=True)

    active = fields.Boolean(default=True, tracking=True)


    # Contacts et responsables
    reconciliation_manager = fields.Char(
        string='Responsable Rapprochement', tracking=True)
    account_manager = fields.Char(string='Chargé clientèle', tracking=True)
    contact = fields.Text(string='Contact', tracking=True,
                          help="Informations de contact supplémentaires de la banque")

    _sql_constraints = [
        ('country_code_uniq', 'unique(country_code)',
         'Le code pays doit être unique !')
    ]

    @api.depends('country_id')
    def _compute_display_name(self):
        for i in self:
            i.display_name = f"{i.name} - {i.country_id.code}"
