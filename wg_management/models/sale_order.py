# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import timedelta

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    def _domain_technicien_ids(self):
        """Domaine pour filtrer les techniciens"""
        group_technicien = self.env.ref('wg_management.group_technicien', raise_if_not_found=False)
        if group_technicien:
            # Obtenir les IDs des utilisateurs qui ont le groupe technicien
            user_ids = group_technicien.user_ids.ids
            if user_ids:
                return [('id', 'in', user_ids)]
        return [('id', '=', False)]  # Aucun utilisateur si le groupe n'existe pas
    
    technicien_ids = fields.Many2many(
        'res.users',
        string='Techniciens',
        help='Techniciens qui vont étudier ce devis'
    )
    
    rejection_motif_id = fields.Many2one(
        'rejection.motif',
        string='Motif de rejet',
        help='Motif de rejet du devis'
    )
    
    longitude = fields.Char(string='Longitude', help='Coordonnée de longitude')
    latitude = fields.Char(string='Latitude', help='Coordonnée de latitude')
    
    address = fields.Char(
        string='Adresse',
    )
    
    hide_prices_for_technicien = fields.Boolean(
        string='Cacher les prix (technicien)',
        compute='_compute_hide_prices_for_technicien',
    )
    
    is_technicien = fields.Boolean(
        string='Est Technicien',
        compute='_compute_is_technicien',
        store=False
    )
    
    @api.depends_context('uid')
    def _compute_is_technicien(self):
        """Vérifie si l'utilisateur connecté est un technicien"""
        for record in self:
            # Vérifier si l'utilisateur a le groupe technicien
            record.is_technicien = self.env.user.has_group('wg_management.group_technicien')

    
    @api.depends()
    def _compute_hide_prices_for_technicien(self):
        is_technicien = self.env.user.has_group('wg_management.group_technicien')
        for order in self:
            order.hide_prices_for_technicien = is_technicien
    
    @api.model_create_multi
    def create(self, vals_list):
        """Créer les activités pour les techniciens lors de la création du devis"""
        orders = super().create(vals_list)
        
        for order in orders:
            # Créer les activités pour tous les techniciens du groupe
            order._create_technicien_activities()
        
        return orders
    
    def _create_technicien_activities(self):
        """Créer les activités pour tous les utilisateurs ayant le rôle technicien"""
        # Récupérer tous les utilisateurs du groupe technicien
        group_technicien = self.env.ref('wg_management.group_technicien', raise_if_not_found=False)
        if not group_technicien or not group_technicien.user_ids:
            return
        
        # Type d'activité par défaut
        activity_type = self.env.ref('mail.mail_activity_data_todo', raise_if_not_found=False)
        if not activity_type:
            return
        
        # Modèle sale.order avec sudo() pour éviter les problèmes d'accès
        res_model = self.env['ir.model'].sudo().search([('model', '=', 'sale.order')], limit=1)
        if not res_model:
            return
        
        for technicien in group_technicien.user_ids:
            # Créer l'activité pour chaque technicien
            self.env['mail.activity'].create({
                'activity_type_id': activity_type.id,
                'summary': f'Étudier le devis {self.name}',
                'note': f'Veuillez étudier et confirmer ou rejeter le devis {self.name} pour le client {self.partner_id.name}.',
                'user_id': technicien.id,
                'res_id': self.id,
                'res_model_id': res_model.id,
                'date_deadline': fields.Date.today(),
            })
    
    def action_confirm(self):
        """Surcharger pour vérifier que seul un technicien peut confirmer et créer une activité pour le commercial"""
        # Vérifier que l'utilisateur a le groupe technicien
        group_technicien = self.env.ref('wg_management.group_technicien', raise_if_not_found=False)
        if not group_technicien or self.env.user.id not in group_technicien.user_ids.ids:
            raise UserError("Seuls les techniciens peuvent confirmer un devis.")
        
        result = super().action_confirm()
        
        # Créer une activité pour le commercial qui a créé le devis
        for order in self:
            if order.create_uid and order.create_uid.id != self.env.user.id:
                # Type d'activité par défaut
                activity_type = self.env.ref('mail.mail_activity_data_todo', raise_if_not_found=False)
                if activity_type:
                    # Modèle sale.order avec sudo() pour éviter les problèmes d'accès
                    res_model = self.env['ir.model'].sudo().search([('model', '=', 'sale.order')], limit=1)
                    
                    if res_model:
                        # Créer l'activité pour le commercial
                        self.env['mail.activity'].create({
                            'activity_type_id': activity_type.id,
                            'summary': f'Devis {order.name} confirmé par le technicien',
                            'note': f'Le devis {order.name} pour le client {order.partner_id.name} a été confirmé par le technicien {self.env.user.name}. Veuillez créer la facture correspondante.',
                            'user_id': order.create_uid.id,
                            'res_id': order.id,
                            'res_model_id': res_model.id,
                            'date_deadline': fields.Date.today() + timedelta(days=1),
                        })
        
        return result
    
    def action_cancel(self):
        """Surcharger pour vérifier que le motif est renseigné avant d'annuler"""
        for order in self:
            if not order.rejection_motif_id:
                raise UserError("Le motif de rejet est obligatoire pour annuler un devis.")
        
        return super().action_cancel()

