# -*- coding: utf-8 -*-

from odoo import models, fields

class AppService(models.Model):
    _name = 'app.service'
    _description = "Les services de l'application"

    name = fields.Char(string="Nom du service", required=True)
    state = fields.Boolean(string="L'etat du service")
    description = fields.Char(string="Description du service")
    image = fields.Binary(string="L'image du service")
    image_name = fields.Char(string="Le nom de l'image")
    is_primary = fields.Boolean(string="Est un service principal")
    type = fields.Selection([('ride', 'Ride'), ('food', 'Food'), ('delivery', 'Delivery'), ('other', 'Other')], string="Type de service", default='ride', required=True)