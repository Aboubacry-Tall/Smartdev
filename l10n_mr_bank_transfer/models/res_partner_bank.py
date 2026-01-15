from odoo import models, fields


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    # Le champ employee_salary_amount existe déjà dans le module hr standard d'Odoo
    # Pas besoin de le redéfinir ici
