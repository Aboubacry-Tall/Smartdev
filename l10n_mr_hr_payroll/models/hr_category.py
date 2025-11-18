
from odoo import fields, models


class HrCategorie(models.Model):
    _name = 'hr.category'
    _description = 'Category'

    name = fields.Char(required=True)
    salary_min = fields.Float(string="Mininum salary" , required=True)
    # Primes
    p_transport = fields.Float(string="Transport")
    p_telephone = fields.Float(string="Prime de telephone")
    p_logt = fields.Float(string="Prime de logment")
    p_eau_electricite = fields.Float(string="Eau et elect")
    
    




