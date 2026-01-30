{
    'name': 'l10n_transfert',
    'summary': 'Menus Virements (Devises, Comptes bancaires, Banques, Employés, Lots, Virement)',
    'description': 'Module fournissant la structure de menus Virements identique à l10n_mr_bank_transfer.',
    'category': 'Accounting/Localizations',
    'version': '19.0.1.0.0',
    'author': 'Smart Odoo Store',
    'depends': ['base', 'hr', 'l10n_mr_bank_transfer'],
    'data': [
        'views/menu.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
