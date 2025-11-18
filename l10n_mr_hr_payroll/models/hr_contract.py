# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class HrContract(models.Model):
    _inherit = 'hr.version'

    l10n_mr_kilometric_exemption = fields.Monetary(
        string='Kilometric Exemption',
        tracking=True)
    l10n_mr_transport_exemption = fields.Monetary(
        string='Transportation Exemption',
        tracking=True)
    l10n_mr_hra = fields.Monetary(
        string='HRA', tracking=True, help="House rent allowance.")
    l10n_mr_da = fields.Monetary(string="DA", help="Dearness allowance")
    l10n_mr_meal_allowance = fields.Monetary(
        string="Meal Allowance", help="Meal allowance")
    l10n_mr_medical_allowance = fields.Monetary(
        string="Medical Allowance", help="Medical allowance")
    l10n_mr_Differentiel = fields.Monetary(string="Différentiel")

    l10n_mr_RSM = fields.Monetary(string="RSM", tracking=True)
    l10n_mr_RITS = fields.Monetary(string="RITS", tracking=True)
    l10n_mr_Production_technique = fields.Monetary(string="Production technique", tracking=True)
    l10n_mr_Telephone = fields.Monetary(string="Téléphone", tracking=True)
    l10n_mr_Interimaire = fields.Monetary(string="Intérimaire", tracking=True)
    l10n_mr_PUV = fields.Monetary(string="PUV", tracking=True)
    l10n_mr_Responsabilite = fields.Monetary(string="Responsabilité", tracking=True)
    l10n_mr_Astreinte = fields.Monetary(string="Astreinte", tracking=True)
    l10n_mr_Risque = fields.Monetary(string="Risque", tracking=True)
    l10n_mr_Eloignement = fields.Monetary(string="Eloignement", tracking=True)
    l10n_mr_Charges_locales = fields.Monetary(string="Charges locales", tracking=True)
    l10n_mr_Technicite = fields.Monetary(string="Technicité", tracking=True)
    l10n_mr_saisie = fields.Monetary(string="SAISIE ", tracking=True)
    l10n_mr_transporter_par = fields.Boolean(string="Transporte par la societe ", tracking=True)
    l10n_mr_sursalaire = fields.Monetary(
        string="Sur salaire ", tracking=True)
    

    category_id = fields.Many2one(
        'hr.category', required=True, help="Category of this contract", tracking=True)
    echallon_id = fields.Many2one(
        'hr.echallon', required=True, help="Echallon of this contract", tracking=True,)

    @api.onchange('echallon_id')
    def _onchange_echallon_id(self):
        for rec in self:
            rec.wage = rec.echallon_id.salary

    @api.constrains('echallon_id', 'category_id')
    def _constrain_category_ech(self):
        for rec in self:
            if rec.echallon_id.category != rec.category_id:
                raise UserError(
                    _("Léchelon doivent être du même catégorie."))
