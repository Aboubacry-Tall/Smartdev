# -*- coding: utf-8 -*-
from odoo import models, fields

class RejectionMotif(models.Model):
    _name = 'rejection.motif'
    _description = 'Motifs de rejet des devis'
    _rec_name = 'name'

    name = fields.Char(string='Motif', required=True)
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Actif', default=True)

