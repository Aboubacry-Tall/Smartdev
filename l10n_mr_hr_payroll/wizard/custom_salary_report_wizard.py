from odoo import models, fields, api


class CustomSalaryReportWizard(models.TransientModel):
    _name = 'custom.salary.report.wizard'
    _description = 'Custom Salary Report Wizard'

    date_start = fields.Date('Date Start', required=True)
    date_end = fields.Date('Date End', required=True)
    bank_ids = fields.Many2many(
        'res.bank', string='Banks', default=lambda self: self.env['res.bank'].search([]))

    def generate_report(self):
        return self.env.ref('l10n_mr_hr_payroll.action_report_hr_payslip_run_bq').report_action(self)
