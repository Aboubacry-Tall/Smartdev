from odoo import models, fields

class HrContract(models.Model):
    _inherit = 'hr.contract'
    
    category_id = fields.Many2one('hr.contract.category', string='Category')

class HrContractCategory(models.Model):
    _name = 'hr.contract.category'

    name = fields.Char(string='Nom')