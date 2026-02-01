# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

class BusActivity(models.Model):
    _name = 'bus.activity'
    _description = 'Bus Activity'
    _order = 'create_date desc'

    name = fields.Char(string='Name', required=True)
    description = fields.Char(string='Description')
    recipient_id = fields.Many2one('res.partner', string='Recipient', required=True)
    message = fields.Text(string='Message', required=True)
    notification_type = fields.Selection([
        ('info', 'Information'),
        ('warning', 'Warning'),
        ('success', 'Success'),
        ('error', 'Error')
    ], string='Type', default='info', required=True)
    status = fields.Selection([
        ('unread', 'Unread'),
        ('read', 'Read'),
        ('archived', 'Archived')
    ], string='Status', default='unread', required=True)
    date_sent = fields.Datetime(string='Date Sent', default=fields.Datetime.now, required=True)
    date_read = fields.Datetime(string='Date Read')
    
    def mark_as_read(self):
        self.write({
            'status': 'read',
            'date_read': fields.Datetime.now()
        })

    def archive_notification(self):
        self.write({'status': 'archived'})