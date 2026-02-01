# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request, Response
import json, base64


class ServiceController(http.Controller):

    #Get services
    @http.route('/yaawi/api/v1/services', auth='public', type='http', methods=['GET'], cors='*', csrf=False)
    def get_all_services(self, **kw):
        services = request.env['app.service'].sudo().search([('state', '=', True)])
        
        data_response = [{
            'success': True,
            'id': service.id,
            'name': service.name,
            'state': service.state,
            'description': service.description,
            'image': service.image.decode('utf-8') if service.image else '',
            'image_name': str(service.image_name),
            'is_primary': service.is_primary,
            'type': service.type
        } for service in services]
        
        response = Response(json.dumps(data_response), content_type="application/json", status=200)
        return response
    
    #Get primary services
    @http.route('/yaawi/api/v1/services/primary', auth='public', type='http', methods=['GET'], cors='*', csrf=False)
    def get_primary_services(self, **kw):
        services = request.env['app.service'].sudo().search([('state', '=', True), ('is_primary', '=', True)], limit=3)

        data_response = [{
            'success': True,
            'id': service.id,
            'name': service.name,
            'state': service.state,
            'description': service.description,
            'image': service.image.decode('utf-8') if service.image else '',
            'image_name': str(service.image_name),
            'is_primary': service.is_primary,
            'type': service.type
        } for service in services]
        
        response = Response(json.dumps(data_response), content_type="application/json", status=200)
        return response
    
    #Get services by type
    @http.route('/yaawi/api/v1/services/type/<string:type>', auth='public', type='http', methods=['GET'], cors='*', csrf=False)
    def get_services_by_type(self, type, **kw):
        services = request.env['app.service'].sudo().search([('type', '=', type), ('state', '=', True)])

        data_response = [{
            'success': True,
            'id': service.id,
            'name': service.name,
            'state': service.state,
            'description': service.description,
            'image': service.image.decode('utf-8') if service.image else '',
            'image_name': str(service.image_name),
            'is_primary': service.is_primary,
            'type': service.type
        } for service in services]

        response = Response(json.dumps(data_response), content_type="application/json", status=200)
        return response
    
    #####################################################################################################################
    
    # Test
    @http.route('/yaawi/api/v1/test', auth='public', type='http', methods=['GET'], cors='*', csrf=False)
    def test(self, **kw):
        response = Response(json.dumps({'success': True, 'message': 'Test'}), content_type="application/json", status=200)
        return response
    
    #####################################################################################################################