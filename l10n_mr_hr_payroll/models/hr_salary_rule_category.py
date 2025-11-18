# -*- coding:utf-8 -*-

from odoo import api, fields, models, _

class HrSalaryRuleCategory(models.Model):
    _inherit = 'hr.salary.rule.category'
    
    place = fields.Integer(string='Position', default=100)
    position = fields.Integer(string='Position', default=100)