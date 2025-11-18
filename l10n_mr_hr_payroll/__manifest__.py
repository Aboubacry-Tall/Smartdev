# -*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Mauritania - Payroll',
    'countries': ['mr'],
    'category': 'Human Resources/Payroll',
    'depends': ['hr_payroll'],
    'version': '1.0',
    'description': """
Mauritania Payroll Rules.
=========================

    * Employee Details
    * Employee Contracts
    """,
    'data': [
        'security/ir.model.access.csv',
        # 'wizard/custom_salary_report_wizard.xml',
        'hr_payroll_reports/hr_payroll_reports.xml',
        # 'hr_payroll_reports/hr_payslips_banques_reports.xml',
        # 'hr_payroll_reports/custom_salary_rules_report.xml',
        'hr_payroll_reports/ir_action_report.xml',
        'hr_payroll_reports/custom_salary_report_template.xml',
        'hr_payroll_reports/report_its.xml',
        'hr_payroll_reports/report_cnam.xml',
        'hr_payroll_reports/report_cnss.xml',
        'hr_payroll_reports/report_etat1.xml',
        'hr_payroll_reports/report_etat2.xml',
        'hr_payroll_reports/its_payslip.xml',
        'hr_payroll_reports/cnam_payslip.xml',
        'hr_payroll_reports/cnss_payslip.xml',
        'hr_payroll_reports/etat1_payslip.xml',
        'hr_payroll_reports/etat2_payslip.xml',
        # 'hr_payroll_reports/journal_ctr_payslip.xml',
        'data/hr_contract_type_data.xml',
        'data/hr_salary_rule_category_data.xml',
        'data/hr_payroll_structure_type_data.xml',
        'data/hr_payroll_structure_data.xml',
        'data/res_partner_data.xml',
        'data/hr_echallon_data.xml',
        'data/hr_rule_parameters_data.xml',
        'data/hr_salary_rule_data.xml',
        'data/hr_payslip_input_type_data.xml',
        'views/hr_contract_views.xml',
        'views/hr_employee_views.xml',
        'views/res_config_settings_views.xml',
        'views/report_payslip_templates.xml',
        
        'views/hr_echallon_views.xml',
        'views/hr_job_view.xml',
        'views/hr_payslips.xml',
        'views/hr_salary_rule_category_views.xml'
        # 'views/hr_payslip_run.xml',

    ],
    'demo': [
        # 'data/l10n_mr_hr_payroll_demo.xml',
    ],
    'author': 'Odoo Community',
    'license': 'OEEL-1',
}
