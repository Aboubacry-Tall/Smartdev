# -*- coding: utf-8 -*-

from odoo import models, fields

class FleetVehicle(models.Model):
    _name = 'fleet.car'
    _description = "Voiture des coursiers"

    driver_id = fields.Many2one('res.partner', string='Propriétaire')
    seats = fields.Integer(string='Nombre de sièges')