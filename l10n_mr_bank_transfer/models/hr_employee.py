from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    matricule = fields.Char(string='Matricule', default='MR-0000')

