# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    email = fields.Char(string="Adresse E-mail", compute='_compute_email', store=True)
    rating = fields.Float(string="Note moyenne reçue", default=1.0)
    state = fields.Selection([('draft', 'En attente'), ('valid', 'Validé'), ('confirm', 'Confirmé'), ('certif', 'Certifié')], string="Status du chauffeur")
    is_driver = fields.Boolean(string='Est un Chauffeur', default=False)
    is_active_driver = fields.Boolean(string="En circulation", default=False)
    license_number = fields.Char(string='Numéro de permis')
    vehicle_id = fields.Many2one('fleet.car', string='Véhicule')
    google_id = fields.Char(string="Google ID", help="Identifiant unique Google")
    google_name = fields.Char(string="Google Name")
    google_photo = fields.Char(string="Google Photo", help="URL de la photo de profil Google")
    google_email = fields.Char(string="Google Email", help="Adresse e-mail associée à Google")
    apple_id = fields.Char(string="Apple ID", help="Identifiant unique Apple")
    apple_name = fields.Char(string="Apple Name")
    apple_email = fields.Char(string="Apple Email", help="Adresse e-mail associée à Apple")
    apple_photo = fields.Char(string="Apple Photo", help="URL de la photo de profil Apple")
    password = fields.Char(string="Mot de passe", help="Mot de passe pour l'authentification")
    identity_file = fields.Binary(string="Carte d'identité", help="Fichier de la carte d'identité du chauffeur")
    license_file = fields.Binary(string="Permis de conduire", help="Fichier du permis de conduire du chauffeur")
    document_file = fields.Binary(string="Autres documents", help="Autres fichiers nécessaires pour le chauffeur")
    vehicle_file = fields.Binary(string="Véhicule", help="Photos du véhicule du chauffeur")
    assurance_file = fields.Binary(string="Assurance", help="Fichier de l'assurance du véhicule du chauffeur")
    is_identity_validated = fields.Boolean(string="Carte d'identité validée", default=False)
    is_license_validated = fields.Boolean(string="Permis de conduire validé", default=False)
    is_document_validated = fields.Boolean(string="Autres documents validés", default=False)
    is_vehicle_validated = fields.Boolean(string="Véhicule validé", default=False)
    is_assurance_validated = fields.Boolean(string="Assurance validée", default=False)
    is_verified = fields.Boolean(string="Vérifié", compute='_compute_is_verified')
                          
    @api.depends('google_email', 'apple_email')
    def _compute_email(self):
        for record in self:
            if record.google_email:
                record.email = record.google_email
            elif record.apple_email:
                record.email = record.apple_email
            else:
                record.email = False 
                
    
    @api.depends('is_identity_validated', 'is_license_validated', 'is_document_validated', 'is_vehicle_validated', 'is_assurance_validated')
    def _compute_is_verified(self):
        for record in self:
            record.is_verified = record.is_identity_validated and record.is_license_validated and record.is_document_validated and record.is_vehicle_validated and record.is_assurance_validated