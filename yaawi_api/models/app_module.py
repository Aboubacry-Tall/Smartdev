# -*- coding: utf-8 -*-

from odoo import models, fields

class AppModule(models.Model):
    _name = 'app.module'
    _description = "Les modules de l'application"
    name = fields.Char(string="Nom du module", required=True)
    state = fields.Boolean(string="L'etat du module")
    description = fields.Char(string="Description du module")