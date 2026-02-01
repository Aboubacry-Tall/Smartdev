# -*- coding: utf-8 -*-

from odoo import models, fields, api
import math

class RideOrder(models.Model):
    _name = 'ride.order'
    _description = 'Course VTC & Covoiturage'

    passenger_id = fields.Many2one('res.partner', string='Passager', required=True)
    driver_id = fields.Many2one('res.partner', string='Chauffeur', required=True)
    ride_type = fields.Selection([('vtc', 'VTC'), ('covoiturage', 'Covoiturage')], string='Type de Course', required=True)
    pickup = fields.Char(string='Lieu de départ')
    destination = fields.Char(string='Destination')
    pickup_lat = fields.Float(string='Latitude départ', required=True)
    pickup_lon = fields.Float(string='Longitude départ', required=True)
    destination_lat = fields.Float(string='Latitude destination', required=True)
    destination_lon = fields.Float(string='Longitude destination', required=True)
    start_time = fields.Datetime(string='Heure de départ')
    end_time = fields.Datetime(string="Heure d’arrivée")
    status = fields.Selection([('en_attente', 'En attente'), ('en_cours', 'En cours'), ('terminee', 'Terminée'), ('annulee', 'Annulée')], string='Statut', default='en_attente')
    price = fields.Float(string='Prix total', compute='_compute_price', store=True, default=50)
    payment_status = fields.Selection([('non_paye', 'Non payé'), ('paye', 'Payé'), ('rembourse', 'Remboursé')], string='Statut du paiement', default='non_paye')
    ride_lines = fields.One2many('ride.line', 'ride_id', string='Étapes du trajet')
    seats_available = fields.Integer(string='Places disponibles')
    distance = fields.Float(string="Distance en Km")


    @api.depends('pickup_lat', 'pickup_lon', 'destination_lat', 'destination_lon')
    def _compute_price(self):
        """ Calcule le prix en fonction de la distance entre les coordonnées GPS """
        price_per_km = 50  # Tarif en MRU par kilomètre
        
        for ride in self:
            if ride.pickup_lat and ride.pickup_lon and ride.destination_lat and ride.destination_lon:
                ride.distance = ride._haversine_distance(
                    ride.pickup_lat, ride.pickup_lon, ride.destination_lat, ride.destination_lon
                )

                if ride.distance > 1:
                    ride.price = round(ride.distance * price_per_km)

    def _haversine_distance(self, lat1, lon1, lat2, lon2):
        """ Calcule la distance en km entre deux points GPS en utilisant la formule de Haversine """
        R = 6371  # Rayon de la Terre en km

        # Convertir les degrés en radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

        # Différences de latitude et de longitude
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        # Formule de Haversine
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c  # Distance en kilomètres

        return distance