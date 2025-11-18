# -*- coding: utf-8 -*-

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    days = fields.Integer(string='Days', default=30)
    matricule = fields.Char(related='employee_id.matricule', string='Matricule', store=True)
    t_brut = fields.Monetary(string="Total Salaire Brut", compute='_compute_t_net', currency_field='currency_id', store=True)
    t_net = fields.Monetary(string="Total Net", compute='_compute_t_net', currency_field='currency_id', store=True)
    t_retenue = fields.Monetary(string="Total Retenue", compute='_compute_t_net', currency_field='currency_id', store=True)
    t_other = fields.Monetary(string="Autres attachement", compute='_compute_t_net', currency_field='currency_id', store=True)
    t_net_paid = fields.Monetary(string="Total Net à Payer", compute='_compute_t_net', currency_field='currency_id', store=True) 
    delta_t_brut = fields.Monetary(string="Écart Salaire Brut", currency_field='currency_id', compute="_compute_differences")
    delta_t_net = fields.Monetary(string="Écart Total Net", currency_field='currency_id', compute="_compute_differences")
    delta_t_retenue = fields.Monetary(string="Écart Retenue", currency_field='currency_id', compute="_compute_differences")
    delta_t_other = fields.Monetary(string="Écart Autres", currency_field='currency_id', compute="_compute_differences")
    delta_t_net_paid = fields.Monetary(string="Écart Total Net à Payer", currency_field='currency_id', compute="_compute_differences")


    @api.depends('date_from', 'date_to', 't_brut', 't_net', 't_retenue', 't_other', 't_net_paid')
    def _compute_differences(self):
        for rec in self:
            # Chercher le lot précédent (par date ou par id décroissant)
            previous_run = self.env['hr.payslip.run'].search([
                ('date_end', '<', rec.payslip_run_id.date_start)
            ], order='date_end desc', limit=1)
            previous_payslip = self.env['hr.payslip'].search([
                ('employee_id', '=', rec.employee_id.id),
                ('payslip_run_id', '=', previous_run.id)
            ], limit=1) if previous_run else False

            rec.delta_t_brut = rec.t_brut - previous_payslip.t_brut if previous_payslip else 0.0
            rec.delta_t_net = rec.t_net - previous_payslip.t_net if previous_payslip else 0.0
            rec.delta_t_retenue = rec.t_retenue - previous_payslip.t_retenue if previous_payslip else 0.0
            rec.delta_t_other = rec.t_other - previous_payslip.t_other if previous_payslip else 0.0
            rec.delta_t_net_paid = rec.t_net_paid - previous_payslip.t_net_paid if previous_payslip else 0.0

    @api.depends('line_ids.amount')
    def _compute_t_net(self):
        for rec in self:
            salaire = 0.0
            cotisation = 0.0
            impot = 0.0
            primes = 0.0
            retenue = 0.0
            other = 0.0
            for line in rec.line_ids:
                if line.appears_on_payslip and line.code in ['SB-C', 'SS-C', 'IL-C', 'IT-C','PR-C', 'PF-C', 'PP-C', 'PH-C']:
                    salaire += line.amount
                if line.appears_on_payslip and line.code in ['CNSS', 'CNAM']:
                    cotisation += line.amount
                if line.appears_on_payslip and line.code in ['ITS']:
                    impot += line.amount
                if line.appears_on_payslip and line.code in ['PPYV', 'PRCH', 'PPRJ', 'PRG1']:
                    primes += line.amount
                if line.appears_on_payslip and line.code in ['PRET', 'AVN']:
                    retenue += line.amount
                if line.appears_on_payslip and line.code in ['RPPL', 'MSSN', 'ALLC', 'MTVT', 'CMMSS', 'CG1', 'PR-A']:
                    other += line.amount

            if rec.days > 0:
                rec.t_brut = ((salaire + primes) / rec.days) * 30
            else:
                rec.t_brut = 0.0
            
            rec.t_net = salaire + primes
            rec.t_retenue = retenue
            rec.t_other = other
            rec.t_net_paid = salaire + primes + retenue + other 

    def print_bank_journal(self):
        selected_payslips = self.browse(self.env.context.get('active_ids'))
        return self.env.ref('smart_payroll.bank_salary_report').report_action(selected_payslips)
