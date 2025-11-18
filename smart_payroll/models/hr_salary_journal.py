from odoo import models, fields, api

class HrSalaryJournal(models.Model):
    _name = 'hr.salary.journal'
    _description = 'Journal de salaire'

    name = fields.Char(string='Nom', required=True)
    date_from = fields.Date(string='Date de début', required=True)
    date_to = fields.Date(string='Date de fin', required=True)
    

    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('verify', 'Confirmé'),
        ('done', 'Approuvé'),
    ], default='draft')

    payslip_run_id = fields.Many2one(
        'hr.payslip.run',
        string='Payslips',
        ondelete='cascade', 
    )

    payslip_ids = fields.One2many(
        related='payslip_run_id.slip_ids',
    )
    
    payslip_count = fields.Integer(default=lambda self: len(self.payslip_ids), compute='_compute_payslip_count', store=False)

    def _compute_payslip_count(self):
        for journal in self:
            journal.payslip_count = len(self.payslip_ids)

    def action_validate(self):
        self.state = 'verify'

    def action_approuvate(self):
        self.state = 'done'

    def action_draft(self):
        self.state = 'draft'

    def action_open_salary_journal(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Journals de salaires',
            'view_mode': 'list',
            'res_model': 'hr.payslip',
            'views': [(self.env.ref('smart_payroll.view_hr_salary_payslip_list').id, 'list')],
            'domain': [('id', 'in', self.payslip_ids.ids)],
            'context': {'salary_journal': True, 'create': False}
        }

    def action_open_bank_journal(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Journals de banques',
            'view_mode': 'list',
            'res_model': 'hr.payslip',
            'views': [(self.env.ref('smart_payroll.view_hr_salary_payslip_list').id, 'list')],
            'domain': [('id', 'in', self.payslip_ids.ids)],
            'context': {'bank_journal': True, 'create': False}
        }
    
    def action_open_control_journal(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Journals de contrôles',
            'view_mode': 'list',
            'res_model': 'hr.payslip',
            'views': [(self.env.ref('smart_payroll.view_hr_salary_payslip_list').id, 'list')],
            'domain': [('id', 'in', self.payslip_ids.ids)],
            'context': {'control_journal': True, 'create': False}
        }