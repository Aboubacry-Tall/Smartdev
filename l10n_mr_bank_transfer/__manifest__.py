{
    'name': 'Virement Bancaire',
    'summary': 'Module pour gérer le journal de virement bancaire',
    'description': 'Module pour gérer le journal de virement bancaire avec les informations des employés',
    'category': 'Human Resources/Payroll',
    'country': 'Mauritania',
    'author': 'Smart Odoo Store',
    'depends': ['hr_payroll', 'hr', 'mail'],
    'data': [
        'data/sequence.xml',
        'security/ir.model.access.csv',
        'views/bank_transfer_batch_wizard_views.xml',
        'views/bank_transfer_batch_views.xml',
        'views/bank_transfer_views.xml',
        'views/bank_transfer_reports.xml',
        'views/menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'l10n_mr_bank_transfer/static/src/scss/bank_transfer_batch.scss',
            'l10n_mr_bank_transfer/static/src/js/bank_transfer_batch_kanban.js',
            'l10n_mr_bank_transfer/static/src/js/bank_transfer_batch_list.js',
            'l10n_mr_bank_transfer/static/src/js/bank_transfer_version_list_controller.js',
            'l10n_mr_bank_transfer/static/src/js/bank_transfer_batch_list_view.js',
            'l10n_mr_bank_transfer/static/src/xml/bank_transfer_version_list_controller.xml',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'sequence': 3,
}

