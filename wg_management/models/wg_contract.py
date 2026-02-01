# -*- coding: utf-8 -*-
from datetime import date
from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
import logging

_logger = logging.getLogger(__name__)

class WgContract(models.Model):
    _name = 'wg.contract'
    _description = 'Contrat Internet'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'
    
    name = fields.Char(string='Numéro de contrat', required=True, default=lambda self: _('New'), readonly=True)
    partner_id = fields.Many2one('res.partner', string='Client', required=True, tracking=True, index=True)
    invoice_ids = fields.Many2many('account.move', string='Factures', help='Factures associées à ce contrat')
    invoice_id = fields.Many2one('account.move', string='Facture d\'origine', help='Facture qui a généré ce contrat', tracking=True)
    sale_order_id = fields.Many2one('sale.order', string='Devis d\'origine', compute='_compute_sale_order_id', store=True)
    start_date = fields.Date(string='Date de début', default=fields.Date.today, required=True, tracking=True)
    end_date = fields.Date(string='Date de fin', compute='_compute_end_date', store=True, tracking=True)
    duration_months = fields.Integer(string='Durée (mois)', default=1, required=True, tracking=True)
    product_id = fields.Many2one('product.product', string='Produit', required=True, tracking=True, 
                                  domain=[('sale_ok', '=', True)], help='Produit associé au contrat')
    currency_id = fields.Many2one('res.currency', string='Devise', default=lambda self: self.env.company.currency_id, required=True)
    monthly_price = fields.Monetary(string='Prix mensuel', compute='_compute_monthly_price', store=False, tracking=True, currency_field='currency_id')
    total_price = fields.Monetary(string='Prix total', compute='_compute_total_price', store=False, currency_field='currency_id')
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('active', 'Actif'),
        ('expired', 'Expiré'),
        ('resilie', 'Résilié'),
        ('cancelled', 'Annulé')
    ], string='État', default='draft', required=True, tracking=True)
    notes = fields.Text(string='Notes')
    intervention_ids = fields.One2many('wg.intervention', 'contract_id', string='Interventions')
    intervention_count = fields.Integer(string='Nombre d\'interventions', compute='_compute_intervention_count')
    invoice_count = fields.Integer(string='Nombre de factures', compute='_compute_invoice_count')
    
    @api.depends('intervention_ids')
    def _compute_intervention_count(self):
        """Calculer le nombre d'interventions pour le smart button"""
        for contract in self:
            contract.intervention_count = len(contract.intervention_ids)
    
    @api.depends('invoice_ids')
    def _compute_invoice_count(self):
        """Calculer le nombre de factures pour le smart button"""
        for contract in self:
            contract.invoice_count = len(contract.invoice_ids)
    
    def action_view_invoices(self):
        """Action pour ouvrir les factures du contrat"""
        self.ensure_one()
        action = {
            'name': 'Factures',
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.invoice_ids.ids)],
            'context': {'default_partner_id': self.partner_id.id},
        }
        if len(self.invoice_ids) == 1:
            action['view_mode'] = 'form'
            action['res_id'] = self.invoice_ids.id
        return action
    
    def action_view_interventions(self):
        """Action pour ouvrir les interventions du contrat"""
        self.ensure_one()
        action = {
            'name': 'Interventions',
            'type': 'ir.actions.act_window',
            'res_model': 'wg.intervention',
            'view_mode': 'list,form',
            'domain': [('contract_id', '=', self.id)],
            'context': {'default_contract_id': self.id, 'default_partner_id': self.partner_id.id},
        }
        if len(self.intervention_ids) == 1:
            action['view_mode'] = 'form'
            action['res_id'] = self.intervention_ids.id
        return action
    
    @api.depends('invoice_id')
    def _compute_sale_order_id(self):
        """Calculer le devis depuis la facture"""
        for contract in self:
            if contract.invoice_id:
                sale_order = contract.invoice_id.invoice_line_ids.mapped('sale_line_ids.order_id')
                contract.sale_order_id = sale_order[0] if sale_order else False
            else:
                contract.sale_order_id = False
    
    
    def _compute_monthly_price(self):
        """Calculer le prix mensuel à partir du prix du produit"""
        for contract in self:
            if contract.product_id:
                contract.monthly_price = contract.product_id.lst_price
            else:
                contract.monthly_price = 0.0
    
    @api.depends('monthly_price', 'duration_months')
    def _compute_total_price(self):
        """Calculer le prix total (prix mensuel * durée)"""
        for contract in self:
            contract.total_price = contract.monthly_price * contract.duration_months
    
    @api.model_create_multi
    def create(self, vals_list):
        """Créer les contrats avec numérotation automatique et calcul de la date de fin"""
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('wg.contract') or _('New')
            # Calculer la date de fin si start_date et duration_months sont présents
            if vals.get('start_date') and vals.get('duration_months'):
                start_date = fields.Date.from_string(vals['start_date'])
                end_date = start_date + relativedelta(months=vals['duration_months'])
                vals['end_date'] = fields.Date.to_string(end_date)
        return super().create(vals_list)
    
    @api.depends('start_date', 'duration_months')
    def _compute_end_date(self):
        """Calculer la date de fin basée sur la date de début et la durée"""
        for contract in self:
            if contract.start_date and contract.duration_months:
                contract.end_date = contract.start_date + relativedelta(months=contract.duration_months)
            else:
                contract.end_date = False
    
    def action_activate(self):
        """Activer le contrat"""
        self.write({'state': 'active'})
    
    def action_cancel(self):
        """Annuler le contrat"""
        self.write({'state': 'cancelled'})
    
    def action_resiliate(self):
        """Résilier le contrat"""
        self.write({'state': 'resilie'})
    
    def action_print_contract(self):
        """Action pour imprimer le contrat"""
        self.ensure_one()
        return self.env.ref('wg_management.report_contract').report_action(self)

    def _has_invoice_for_month(self, year, month):
        """Vérifie si le contrat a déjà une facture pour le mois donné."""
        self.ensure_one()
        if not self.invoice_ids:
            return False
        for inv in self.invoice_ids:
            if inv.invoice_date and inv.invoice_date.year == year and inv.invoice_date.month == month:
                return True
        return False

    def _create_monthly_invoice(self, invoice_date):
        """Crée une facture mensuelle pour ce contrat à la date donnée."""
        self.ensure_one()
        if not self.product_id:
            raise UserError(_("Le contrat %s n'a pas de produit défini.") % self.name)
        price_unit = self.product_id.lst_price
        line_name = _("%s - %s") % (self.product_id.name, invoice_date.strftime("%Y-%m"))
        move_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'invoice_date': invoice_date,
            'ref': _("%s - %s") % (self.name, invoice_date.strftime("%Y-%m")),
            'invoice_line_ids': [
                (0, 0, {
                    'product_id': self.product_id.id,
                    'quantity': 1,
                    'price_unit': price_unit,
                    'name': line_name,
                }),
            ],
        }
        move = self.env['account.move'].with_context(default_move_type='out_invoice').create(move_vals)
        self.write({'invoice_ids': [(4, move.id)]})
        _logger.info("Facture mensuelle créée: %s pour le contrat %s", move.name, self.name)
        return move

    @api.model
    def cron_generate_monthly_invoices(self):
        """
        Cron exécuté le 1er de chaque mois.
        Génère une facture pour chaque contrat actif qui n'a pas encore de facture pour le mois en cours.
        """
        today = date.today()
        if today.day != 1:
            _logger.debug("cron_generate_monthly_invoices: pas le 1er du mois, ignoré.")
            return
        contracts = self.search([('state', '=', 'active')])
        created = 0
        for contract in contracts:
            # Ne pas générer si le contrat est déjà expiré à cette date
            if contract.end_date and contract.end_date < today:
                continue
            if contract._has_invoice_for_month(today.year, today.month):
                continue
            try:
                contract._create_monthly_invoice(today)
                created += 1
            except Exception as e:
                _logger.exception("Erreur création facture mensuelle pour contrat %s: %s", contract.name, e)
        _logger.info("cron_generate_monthly_invoices: %s facture(s) créée(s) pour %s contrat(s) actifs.", created, len(contracts))

