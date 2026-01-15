{
    'name': 'Gestion des Virements SOGEM',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Gestion des virements simples et multiples SOGEM',
    'description': """
        Module de gestion des virements pour SOGEM permettant de :
        - Gérer les comptes bancaires SOGEM
        - Gérer les bénéficiaires
        - Effectuer des virements simples et multiples
        - Suivre le statut des virements
        - Analyser l'historique des virements
        - Consulter les statistiques détaillées
    """,
    'author': 'SMART MS',
    'website': 'https://smartmssa.com',
    'icon': '/odoo_virements/static/description/icon.svg',
    'depends': ['base', 'account', 'mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/import_transfer_lines_wizard_view.xml',
        'views/account_bank_views.xml',
        'views/beneficiary_views.xml',
        'views/transfer_views.xml',
        'views/transfer_report_views.xml',
        'views/sogem_bank.xml',
        'views/category_views.xml',
        'report/international_transfere.xml',
        'views/menu_views.xml',
        'report/transfer_report.xml',

        
        'data/sequence.xml',
        
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
