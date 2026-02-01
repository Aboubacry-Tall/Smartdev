# -*- coding: utf-8 -*-
{
    'name': "wg_management",

    'summary': "Module de gestion avec rôles (Commercial, Technicien, Financier)",

    'description': """
Module de gestion avec rôles personnalisés
==========================================
Ce module définit trois rôles principaux :
- Commercial
- Technicien
- Financier
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management', 'mail', 'account', 'product'],

    # always loaded
    'data': [
        'security/wg_management_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/ir_cron_monthly_invoices.xml',
        'reports/contract_report.xml',
        'views/rejection_motif.xml',
        'views/sale_order.xml',
        'views/wg_contract.xml',
        'views/res_partner.xml',
        'views/account_move.xml',
        'views/account_payment.xml',
        'views/account_payment_register.xml',
        'views/wg_intervention.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}

