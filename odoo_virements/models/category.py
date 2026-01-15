# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BeneficiaryCategory(models.Model):
    _name = 'beneficiary.category'
    _description = 'Catégorie de Bénéficiaire'
    _order = 'name'

    name = fields.Char(
        string='Nom de la Catégorie',
        required=True,
        translate=True
    )
    
    description = fields.Text(
        string='Description',
        translate=True
    )
    
    beneficiary_ids = fields.One2many(
        'sogem.beneficiary',
        'category_id',
        string='Bénéficiaires'
    )
    
    beneficiary_count = fields.Integer(
        string='Nombre de Bénéficiaires',
        compute='_compute_beneficiary_count'
    )

    @api.depends('beneficiary_ids')
    def _compute_beneficiary_count(self):
        for category in self:
            category.beneficiary_count = len(category.beneficiary_ids)

    def name_get(self):
        """Return the display name for the category"""
        result = []
        for record in self:
            name = record.name or 'Sans nom'
            result.append((record.id, name))
        return result

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        if name:
            categories = self.search([
                ('name', operator, name)
            ] + args, limit=limit)
            return categories.name_get()
        return super(BeneficiaryCategory, self).name_search(name, args, operator, limit)

    def action_view_beneficiaries(self):
        """Action pour voir les bénéficiaires de cette catégorie"""
        action = self.env.ref('odoo_virements.action_sogem_beneficiary').read()[0]
        action['domain'] = [('category_id', '=', self.id)]
        action['context'] = {'default_category_id': self.id}
        return action
