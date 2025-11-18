
from odoo import fields, models, api


class HrEchallon(models.Model):
    _name= 'hr.echallon'
    _description = 'Echallon'

    name = fields.Char(required=True, help="Name of this echallons")
    salary = fields.Monetary(
        currency_field='currency_id',
        string="salary", required=True, help="Base salary of this echallons")
    category = fields.Many2one("hr.category",required=True, help="Category of this echallon")
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        compute='_compute_currency_id',
        store=True,
        readonly=False,
    )
  
    
    @api.depends_context('allowed_company_ids')
    def _compute_currency_id(self):
        self.currency_id = self.env.company.currency_id
