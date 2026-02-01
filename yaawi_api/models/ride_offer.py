# -*- coding: utf-8 -*-

from odoo import models, fields

class RideOffer(models.Model):
    _name = 'ride.offer'
    _description = 'Offre de Covoiturage'

    driver_id = fields.Many2one('res.partner', string='Conducteur', required=True)
    pickup = fields.Char(string='Lieu de départ', required=True)
    destination = fields.Char(string='Destination', required=True)
    start_time = fields.Datetime(string='Heure de départ')
    seats_available = fields.Integer(string='Places disponibles', required=True)
    price_per_seat = fields.Float(string='Prix par place', required=True)
    status = fields.Selection([('ouvert', 'Ouvert'), ('complet', 'Complet'), ('annule', 'Annulé')], string='Statut', default='ouvert')