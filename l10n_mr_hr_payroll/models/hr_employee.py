# -*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
from odoo.fields import Domain


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    l10n_mr_cin_number = fields.Char(
        string="CIN Number", help="National Identity Card Number",groups="hr.group_hr_user")
    l10n_mr_cnss_number = fields.Char(
        string="CNSS Number", help="Social Security National Fund Number",groups="hr.group_hr_user")
    l10n_mr_cimr_number = fields.Char(
        string="CIMR Number", help="Mauritania Interprofessional Retirement Fund",groups="hr.group_hr_user")
    l10n_mr_mut_number = fields.Char(string="Mutual Insurance Number",groups="hr.group_hr_user")
    l10n_mr_matricule = fields.Char(string="Matricule",groups="hr.group_hr_user")
    
    @api.model
    def _name_search(self, name, domain=None, operator='ilike', limit=None, order=None):
        # OVERRIDE
        domain = domain or []
        if operator != 'ilike' or (name or '').strip():
            name_domain = ['|', ('name', 'ilike', name),
                           ('l10n_mr_matricule', '=ilike', name)]
            domain = Domain.AND([name_domain, domain])
        return self._search(domain, limit=limit, order=order)


# Note: The hr.payroll.report model was removed in Odoo 19.0
# The Mauritania-specific fields (l10n_mr_matricule, l10n_mr_cnss_number) 
# are already available in hr.employee and will be accessible in reports
# through standard Odoo 19 reporting mechanisms
