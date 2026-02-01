# -*- coding: utf-8 -*-

from odoo import models, fields, api

class RideReservation(models.Model):
    _name = 'ride.reservation'
    _description = 'Réservation de covoiturage'

    offer_id = fields.Many2one('ride.offer', string='Offre', required=True)
    passenger_id = fields.Many2one('res.partner', string='Passager', required=True)
    seats_reserved = fields.Integer(string='Places réservées', required=True)
    total_price = fields.Float(string='Prix total', compute='_compute_total_price', store=True)
    status = fields.Selection([('en_attente', 'En attente'), ('confirme', 'Confirmé'), ('annule', 'Annulé')], string='Statut', default='en_attente')

    @api.depends('seats_reserved', 'offer_id.price_per_seat')
    def _compute_total_price(self):
        for rec in self:
            rec.total_price = rec.seats_reserved * rec.offer_id.price_per_seat