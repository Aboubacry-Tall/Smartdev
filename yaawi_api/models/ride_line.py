# -*- coding: utf-8 -*-

from odoo import models, fields

class RideLine(models.Model):
    _name = 'ride.line'
    _description = 'Étape du trajet'

    ride_id = fields.Many2one('ride.order', string='Course', required=True)
    location = fields.Char(string='Emplacement', required=True)
    timestamp = fields.Datetime(string='Heure de passage')