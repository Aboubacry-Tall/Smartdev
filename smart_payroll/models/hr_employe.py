from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    matricule = fields.Char(string='Matricule', groups='hr.group_hr_user')
    account_number = fields.Char(string='Compte bancaire', groups='hr.group_hr_user')
    contract_wage = fields.Monetary(related='contract_id.wage', string="Salaire Brut", store=False, groups='hr.group_hr_user')