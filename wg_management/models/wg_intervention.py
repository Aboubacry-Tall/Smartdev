# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _
from datetime import timedelta

class WgIntervention(models.Model):
    _name = 'wg.intervention'
    _description = 'Fiche d\'intervention'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'
    
    @api.model
    def _get_commercial_domain(self):
        """Domaine pour filtrer les commerciaux"""
        group_commercial = self.env.ref('wg_management.group_commercial', raise_if_not_found=False)
        if group_commercial:
            user_ids = group_commercial.user_ids.ids
            if user_ids:
                return [('id', 'in', user_ids)]
        return [('id', '=', False)]
    
    @api.model
    def _get_technicien_domain(self):
        """Domaine pour filtrer les techniciens"""
        group_technicien = self.env.ref('wg_management.group_technicien', raise_if_not_found=False)
        if group_technicien:
            user_ids = group_technicien.user_ids.ids
            if user_ids:
                return [('id', 'in', user_ids)]
        return [('id', '=', False)]
    
    name = fields.Char(string='Numéro d\'intervention', required=True, default=lambda self: _('New'), readonly=True)
    partner_id = fields.Many2one('res.partner', string='Client', required=True, tracking=True, index=True)
    partner_address = fields.Char(string='Adresse du client', related='partner_id.contact_address', readonly=True)
    sale_order_id = fields.Many2one('sale.order', string='Devis', tracking=True, help='Devis associé à cette intervention')
    contract_id = fields.Many2one('wg.contract', string='Contrat', tracking=True, help='Contrat associé à cette intervention')
    commercial_id = fields.Many2one('res.users', string='Commercial', required=True, default=lambda self: self.env.user, tracking=True, domain=_get_commercial_domain)
    technicien_id = fields.Many2one('res.users', string='Technicien', tracking=True, domain=_get_technicien_domain)
    intervention_date = fields.Date(string='Date d\'intervention', default=fields.Date.today, tracking=True)
    intervention_type = fields.Selection([
        ('installation', 'Installation'),
        ('maintenance', 'Maintenance'),
        ('reparation', 'Réparation'),
        ('mise_en_service', 'Mise en service'),
        ('suspension', 'Suspension'),
    ], string='Type d\'intervention', required=True, default='mise_en_service', tracking=True)
    description = fields.Text(string='Description', tracking=True, help='Description de l\'intervention à effectuer')
    notes = fields.Text(string='Notes', help='Notes additionnelles')
    execution_notes = fields.Text(string='Notes d\'exécution', help='Notes sur l\'exécution de l\'intervention')
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('transmitted', 'Transmise au technicien'),
        ('in_progress', 'En cours'),
        ('executed', 'Exécutée'),
        ('confirmed', 'Archivée'),
        ('cancelled', 'Annulée'),
    ], string='État', default='draft', required=True, tracking=True)
    transmission_date = fields.Datetime(string='Date de transmission', readonly=True, tracking=True)
    execution_date = fields.Datetime(string='Date d\'exécution', readonly=True, tracking=True)
    confirmation_date = fields.Datetime(string='Date de confirmation', readonly=True, tracking=True)
    
    @api.model_create_multi
    def create(self, vals_list):
        """Créer les interventions avec numérotation automatique et créer une activité pour le technicien"""
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('wg.intervention') or _('New')
        
        interventions = super().create(vals_list)
        
        for intervention in interventions:
            if intervention.technicien_id:
                intervention._create_technicien_activity()
        
        return interventions
    
    def action_transmit_to_technicien(self):
        """Transmettre l'intervention au technicien"""
        for intervention in self:
            if intervention.state != 'draft':
                raise UserError("Seules les interventions en brouillon peuvent être transmises.")
            
            if not intervention.technicien_id:
                raise UserError("Veuillez sélectionner un technicien avant de transmettre l'intervention.")
            
            # Vérifier que l'utilisateur a le groupe commercial
            group_commercial = self.env.ref('wg_management.group_commercial', raise_if_not_found=False)
            if not group_commercial or self.env.user.id not in group_commercial.user_ids.ids:
                raise UserError("Seuls les commerciaux peuvent transmettre une intervention au technicien.")
            
            # Mettre à jour l'état
            intervention.write({
                'state': 'transmitted',
                'transmission_date': fields.Datetime.now(),
            })
            
            # Créer une activité pour le technicien
            intervention._create_technicien_activity()
    
    def _create_technicien_activity(self):
        """Créer une activité pour le technicien"""
        if not self.technicien_id:
            return
        
        activity_type = self.env.ref('mail.mail_activity_data_todo', raise_if_not_found=False)
        if not activity_type:
            return
        
        res_model = self.env['ir.model'].sudo().search([('model', '=', 'wg.intervention')], limit=1)
        if not res_model:
            return
        
        self.env['mail.activity'].create({
            'activity_type_id': activity_type.id,
            'summary': f'Intervention {self.name} - {self.intervention_type}',
            'note': f'Fiche d\'intervention transmise par {self.commercial_id.name} pour le client {self.partner_id.name}.\n\n{self.description or ""}',
            'user_id': self.technicien_id.id,
            'res_id': self.id,
            'res_model_id': res_model.id,
            'date_deadline': fields.Date.today() + timedelta(days=3),
        })
    
    def action_start_intervention(self):
        """Démarrer l'intervention"""
        for intervention in self:
            if intervention.state != 'transmitted':
                raise UserError("Seules les interventions transmises peuvent être démarrées.")
            
            # Vérifier que l'utilisateur a le groupe technicien
            group_technicien = self.env.ref('wg_management.group_technicien', raise_if_not_found=False)
            if not group_technicien or self.env.user.id not in group_technicien.user_ids.ids:
                raise UserError("Seuls les techniciens peuvent démarrer une intervention.")
            
            intervention.write({'state': 'in_progress'})
    
    def action_confirm_execution(self):
        """Confirmer l'exécution de l'intervention"""
        for intervention in self:
            if intervention.state not in ('transmitted', 'in_progress'):
                raise UserError("Seules les interventions transmises ou en cours peuvent être confirmées comme exécutées.")
            
            # Vérifier que l'utilisateur a le groupe technicien
            group_technicien = self.env.ref('wg_management.group_technicien', raise_if_not_found=False)
            if not group_technicien or self.env.user.id not in group_technicien.user_ids.ids:
                raise UserError("Seuls les techniciens peuvent confirmer l'exécution d'une intervention.")
            
            # Mettre à jour l'état
            intervention.write({
                'state': 'executed',
                'execution_date': fields.Datetime.now(),
            })
            
            # Créer une activité pour le commercial
            intervention._create_commercial_activity()
    
    def _create_commercial_activity(self):
        """Créer une activité pour le commercial pour l'informer de l'exécution"""
        if not self.commercial_id:
            return
        
        activity_type = self.env.ref('mail.mail_activity_data_todo', raise_if_not_found=False)
        if not activity_type:
            return
        
        res_model = self.env['ir.model'].sudo().search([('model', '=', 'wg.intervention')], limit=1)
        if not res_model:
            return
        
        self.env['mail.activity'].create({
            'activity_type_id': activity_type.id,
            'summary': f'Intervention {self.name} exécutée',
            'note': f'L\'intervention {self.name} pour le client {self.partner_id.name} a été exécutée par {self.technicien_id.name if self.technicien_id else "le technicien"}.\n\n{self.execution_notes or ""}',
            'user_id': self.commercial_id.id,
            'res_id': self.id,
            'res_model_id': res_model.id,
            'date_deadline': fields.Date.today() + timedelta(days=1),
        })
    
    def action_confirm(self):
        """Confirmer l'intervention après contact avec le client"""
        for intervention in self:
            if intervention.state != 'executed':
                raise UserError("Seules les interventions exécutées peuvent être confirmées.")
            
            # Vérifier que l'utilisateur a le groupe commercial
            group_commercial = self.env.ref('wg_management.group_commercial', raise_if_not_found=False)
            if not group_commercial or self.env.user.id not in group_commercial.user_ids.ids:
                raise UserError("Seuls les commerciaux peuvent confirmer une intervention après contact avec le client.")
            
            # Mettre à jour l'état
            intervention.write({
                'state': 'confirmed',
                'confirmation_date': fields.Datetime.now(),
            })
    
    def action_cancel(self):
        """Annuler l'intervention"""
        for intervention in self:
            if intervention.state in ('executed', 'confirmed'):
                raise UserError("Impossible d'annuler une intervention déjà exécutée ou confirmée.")
            intervention.write({'state': 'cancelled'})

