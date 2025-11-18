# -*- coding: utf-8 -*-
{
    'name': "smart_payroll",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
        Long description of module's
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr_payroll', 'hr_contract'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/report_payslip_templates.xml',
        'views/hr_payslip_views.xml',
        'views/base_document_layout_views.xml',
        'views/hr_journal_actions.xml',
        'views/hr_journal_menu.xml',
        'views/hr_journal_salary_views.xml',
        'reports/_ir_action_report.xml',
        'reports/hr_bank_report.xml',
        'views/hr_contract_views.xml',
        'reports/hr_control_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'LGPL-3',
}

