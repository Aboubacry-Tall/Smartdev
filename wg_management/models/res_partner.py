# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    contract_ids = fields.One2many('wg.contract', 'partner_id', string='Contrats Internet')
    contract_count = fields.Integer(string='Nombre de contrats', compute='_compute_contract_count')
    nni = fields.Char(string="Numéro National d'identification")
    type_contact = fields.Selection([('A', 'A'), ('B', 'B'), ('C', 'C')], string="Type de Contact")
    is_client = fields.Boolean(string='Client', default=False,
                               help='Coché si ce partenaire est un client (apparaît dans la liste Clients)')
    code = fields.Char(string='Code client', help='Identifiant client (ex: HQ/1, HQ/2...)')
    
    @api.depends('contract_ids')
    def _compute_contract_count(self):
        """Calculer le nombre de contrats pour le smart button"""
        for partner in self:
            partner.contract_count = len(partner.contract_ids)
    
    def action_view_contracts(self):
        """Action pour ouvrir les contrats du client"""
        self.ensure_one()
        action = {
            'name': 'Contrats Internet',
            'type': 'ir.actions.act_window',
            'res_model': 'wg.contract',
            'view_mode': 'list,form',
            'domain': [('partner_id', '=', self.id)],
            'context': {'default_partner_id': self.id},
        }
        if len(self.contract_ids) == 1:
            action['view_mode'] = 'form'
            action['res_id'] = self.contract_ids.id
        return action

