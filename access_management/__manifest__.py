# pylint: disable=pointless-statement
{
    "name": "Gestion des accès",
    "category": "Tools",
    "summary": "Gestion des accès et des profils de sécurité",
    "author": "Smartdev",
    "depends": [
        "base",
        "sale",
        "crm",
        "account",
        "sale_subscription",
        "project",
        "helpdesk",
        "hr",
        "hr_payroll",
        "website",
        "marketing_automation",
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/sale_order_views.xml",
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}

