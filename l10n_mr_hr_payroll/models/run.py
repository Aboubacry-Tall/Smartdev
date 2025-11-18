from odoo import models, fields, api

class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'


    
    def action_print_payslip_report(self):
        return self.env.ref('l10n_mr_hr_payrollt.action_report_hr_payslips_run_its').report_action(self)
    
   