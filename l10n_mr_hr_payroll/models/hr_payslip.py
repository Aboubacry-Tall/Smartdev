# -*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, date




class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def _get_data_files_to_update(self):
        # Note: file order should be maintained
        return super()._get_data_files_to_update() + [(
            'l10n_mr_hr_payroll', [
                'data/hr_salary_rule_category_data.xml',
                'data/hr_payroll_structure_type_data.xml',
                'data/hr_payroll_structure_data.xml',
                'data/hr_rule_parameters_data.xml',
                'data/hr_salary_rule_data.xml',
                'data/hr_payslip_input_type_data.xml',
            ])]
        
    seniority_years = fields.Integer(
        "Seniority Years", compute='_compute_seniority', store=True)
    seniority_months = fields.Integer(
        "Seniority Months", compute='_compute_seniority', store=True)
    seniority_days = fields.Integer(
        "Seniority Days", compute='_compute_seniority', store=True)
    employee_bank_name = fields.Char(
        related='employee_id.primary_bank_account_id.bank_id.name', string='Bank', store=True, readonly=True)


    @api.depends('employee_id', 'version_id', 'version_id.contract_date_start')
    def _compute_seniority(self):
        for payslip in self:
            if payslip.version_id and payslip.version_id.contract_date_start:
                start_date = payslip.version_id.contract_date_start
                # Convert start_date to datetime.date if it's a datetime.datetime
                if isinstance(start_date, datetime):
                    start_date = start_date.date()

                today = date.today()  # Use date.today() to get the current date

                # Calculate the difference
                delta = today - start_date
                years = delta.days // 365
                months = (delta.days % 365) // 30
                days = (delta.days % 365) % 30

                payslip.seniority_years = years
                payslip.seniority_months = months
                payslip.seniority_days = days
            else:
                payslip.seniority_years = 0
                payslip.seniority_months = 0
                payslip.seniority_days = 0
        

    worked_days_custom = fields.Float(string="Worked Days (Custom)", default=30, tracking=True)

    @api.depends('worked_days_custom')
    def compute_basic_salary(self):
        for payslip in self:
            if payslip.worked_days_custom:
                payslip.basic_salary_custom = (
                    payslip.version_id.wage / 30) * payslip.worked_days_custom
            else:
                payslip.basic_salary_custom = payslip.version_id.wage

    basic_salary_custom = fields.Float(
        string="Basic Salary (Custom)", compute="compute_basic_salary", store=True)
    
    def compute_sheet(self):
        for payslip in self:
            codes_entrées = [
                input_line.code for input_line in payslip.input_line_ids]
            entrées_dupliquées = set(
                [code for code in codes_entrées if codes_entrées.count(code) > 1])

            if entrées_dupliquées:
                codes_dupliqués = ', '.join(entrées_dupliquées)
                employe_nom = payslip.employee_id.name
                employe_matricule = payslip.employee_id.l10n_mr_matricule
                raise UserError(
                    _("Des doublons ont été détectés pour les codes suivants : %s pour l'employé : %s Matricule : %s. Veuillez supprimer les doublons avant de continuer.") % (codes_dupliqués, employe_nom, employe_matricule))

        return super(HrPayslip, self).compute_sheet()

    def print_payslips(self):
        return self.env.ref('l10n_mr_hr_payroll.custom_salary_report_d').report_action(self, config=False)
    
    def print_reports(self):
        selected_payslips = self.browse(self.env.context.get('active_ids'))

        return self.env.ref('l10n_mr_hr_payroll.action_report_payslip_ts').report_action(selected_payslips)
    
    def print_reports_cnam(self):
        selected_payslips = self.browse(self.env.context.get('active_ids'))

        return self.env.ref('l10n_mr_hr_payroll.action_report_payslip_cnam').report_action(selected_payslips)
    
    def print_reports_cnss(self):
        selected_payslips = self.browse(self.env.context.get('active_ids'))

        return self.env.ref('l10n_mr_hr_payroll.action_report_payslip_cnss').report_action(selected_payslips)
    
    def print_reports_etat1(self):
        selected_payslips = self.browse(self.env.context.get('active_ids'))
        return self.env.ref('l10n_mr_hr_payroll.action_report_payslip_etat1').report_action(selected_payslips)
    
    def print_reports_control(self):
        return self.env.ref('l10n_mr_hr_payroll.action_report_payslip_journal_ctr').report_action(self, config=False)

    def print_reports_etat2(self):
        selected_payslips = self.browse(self.env.context.get('active_ids'))
        return self.env.ref('l10n_mr_hr_payroll.action_report_payslip_etat2').report_action(selected_payslips)