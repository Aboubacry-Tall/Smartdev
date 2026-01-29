# pylint: disable=pointless-statement
{
    "name": "Gestion des accès",
    "category": "Tools",
    "summary": "Gestion des accès et des profils de sécurité",
    "author": "Smartdev",
    "depends": ["base", "sale"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/sale_order_views.xml",
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}

