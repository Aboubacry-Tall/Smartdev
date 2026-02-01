# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request, Response
import json

class BusActivityController(http.Controller):
    
    # Create a new bus activity
    @http.route('/yaawi/api/v1/activity', auth='public', type='http', methods=['POST'], cors='*', csrf=False)
    def create_activity(self, **kw):
        data = request.get_json_data()
        required_fields = ['name', 'description', 'message', 'notification_type', 'status', 'recipient_id']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return Response(json.dumps({
                'error': 'Champs manquants',
                'missing_fields': missing_fields
            }), content_type='application/json', status=400)
            
        activity = request.env['bus.activity'].sudo().create({
            'name': data['name'],
            'description': data['description'],
            'message': data['message'],
            'notification_type': data['notification_type'],
            'status': data['status'],
            'recipient_id': data['recipient_id']
        })
        
        data_response = {
            'success': True,
            'id': activity.id,
            'name': activity.name,
            'description': activity.description,
            'message': activity.message,
            'notification_type': activity.notification_type,
            'status': activity.status,
            'date_sent': activity.date_sent.isoformat() if activity.date_sent else None
        }
        
        response = Response(json.dumps(data_response), content_type='application/json', status=201)
        return response
    
    # Update an activity
    @http.route('/yaawi/api/v1/activity/<int:activity_id>', auth='public', type='http', methods=['PUT'], cors='*', csrf=False)
    def update_activity(self, activity_id, **kw):
        data = request.get_json_data()
        activity = request.env['bus.activity'].sudo().browse(activity_id)
        if not activity:
            return Response(json.dumps({
               'error': 'Activité non trouvée'
            }), content_type='application/json', status=404)
        activity.write({
            'name': data.get('name', activity.name),
            'description': data.get('description', activity.description),
            'message': data.get('message', activity.message),
            'notification_type': data.get('notification_type', activity.notification_type),
            'status': data.get('status', activity.status),
            'date_read': data.get('date_read', activity.date_read)
        })
        
        data_response = {
           'success': True,
            'id': activity.id,
            'name': activity.name,
            'description': activity.description,
            'message': activity.message,
            'notification_type': activity.notification_type,
            'status': activity.status,
            'date_sent': activity.date_sent.isoformat() if activity.date_sent else None,
            'date_read': activity.date_read.isoformat() if activity.date_read else None
        }
        
        response = Response(json.dumps(data_response), content_type='application/json', status=200)
        return response
    
    # Get partner activities
    @http.route('/yaawi/api/v1/partner/<int:partner_id>/activities', auth='public', type='http', methods=['GET'], cors='*', csrf=False)
    def get_partner_activities(self, partner_id, **kw):
        activities = request.env['bus.activity'].sudo().search([('recipient_id', '=', partner_id)], order='date_sent desc')

        data_response = [{
            'success': True,
            'id': activity.id,
            'name': str(activity.name or ''),
            'description': str(activity.description or ''),
            'message': str(activity.message or ''),
            'notification_type': str(activity.notification_type or 'info'),
            'status': activity.status,
            'date_sent': activity.date_sent.isoformat() if activity.date_sent else None,
            'date_read': activity.date_read.isoformat() if activity.date_read else None
        } for activity in activities]

        response = Response(json.dumps(data_response), content_type='application/json', status=200)
        return response