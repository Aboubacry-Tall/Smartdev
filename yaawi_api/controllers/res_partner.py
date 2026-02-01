# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request, Response
import json

class ResPartnerController(http.Controller):
    
    # Check partner by Google account
    @http.route('/yaawi/api/v1/partner/google', auth='public', type='http', methods=['POST'], cors='*', csrf=False)
    def create_user_google(self, **kw):
       
        data = json.loads(request.httprequest.data)
        
        if not data:
            return Response(json.dumps({'success': False, 'error': 'Invalid JSON data'}), content_type='application/json', status=400)
        
        google_id = data.get('google_id')
        google_email = data.get('google_email')

        if not google_id or not google_email:
            return Response(json.dumps({'success': False, 'error': 'Missing required fields'}), content_type='application/json', status=400)

        # Vérifier si l'utilisateur existe déjà
        user_exist = request.env['res.partner'].sudo().search([
            ('google_id', '=', google_id),
            ('google_email', '=', google_email)
        ], limit=1)

        if user_exist:
            data_response = {
                'success': True,
                'id': user_exist.id,
                'name': user_exist.name,
                'email': str(user_exist.email or user_exist.google_name or ''),
                'google_id': user_exist.google_id,
                'google_name': user_exist.google_name,
                'google_photo': user_exist.google_photo,
                'google_email': user_exist.google_email,
                'rating': user_exist.rating,
                'state': str(user_exist.state or 'draft'),
                'is_driver': user_exist.is_driver,
                'is_active_driver': user_exist.is_active_driver,
                'license_file' : user_exist.license_file.decode('utf-8') if user_exist.license_file else '',
                'document_file' : user_exist.document_file.decode('utf-8') if user_exist.document_file else '',
                'vehicle_file' : user_exist.vehicle_file.decode('utf-8') if user_exist.vehicle_file else '',
                'assurance_file' : user_exist.assurance_file.decode('utf-8') if user_exist.assurance_file else '',
                'is_identity_validated': user_exist.is_identity_validated,
                'is_license_validated': user_exist.is_license_validated,
                'is_document_validated': user_exist.is_document_validated,
                'is_vehicle_validated': user_exist.is_vehicle_validated,
                'is_assurance_validated': user_exist.is_assurance_validated,
                'is_verified': user_exist.is_verified
            }
            response = Response(json.dumps(data_response), content_type="application/json", status=200)
            return response

        # Créer un nouvel utilisateur
        user = request.env['res.partner'].sudo().create({
            'name' : data.get('google_name'),
            'email' : google_email,
            'google_id': google_id,
            'google_name': data.get('google_name'),
            'google_email': google_email,
            'google_photo': data.get('google_photo'),
            'state' : 'draft'
        })

        data_response =  {
            'success': True,
            'id': user.id,
            'name': user.name,
            'email': str(user.email or user.google_email),
            'google_id': user.google_id,
            'google_name': user.google_name,
            'google_email': user.google_email,
            'google_photo': user.google_photo,
            'rating': user.rating,
            'state': str(user.state or 'draft'),
            'is_driver': user.is_driver,
            'is_active_driver': user.is_active_driver,
            'license_file' : user.license_file.decode('utf-8') if user.license_file else '',
            'document_file' : user.document_file.decode('utf-8') if user.document_file else '',
            'vehicle_file' : user.vehicle_file.decode('utf-8') if user.vehicle_file else '',
            'assurance_file' : user.assurance_file.decode('utf-8') if user.assurance_file else '',
            'is_identity_validated': user.is_identity_validated,
            'is_license_validated': user.is_license_validated,
            'is_document_validated': user.is_document_validated,
            'is_vehicle_validated': user.is_vehicle_validated,
            'is_assurance_validated': user.is_assurance_validated,
            'is_verified': user.is_verified
        }
        
        response = Response(json.dumps(data_response), content_type="application/json", status=201)
        return response
    
    # Get partner by id
    @http.route('/yaawi/api/v1/partner/<int:partner_id>', auth='public', type='http', methods=['GET'], cors='*', csrf=False)
    def get_partner_by_id(self, partner_id, **kw):
        partner = request.env['res.partner'].sudo().browse(partner_id)

        if not partner:
            return Response(json.dumps({
                'error': 'Utilisateur introuvable'
            }), content_type='application/json', status=404)
            
        data_response = {
            'success': True,
            'id': partner.id,
            'name': partner.name,
            'email': str(partner.email or partner.google_email or ''),
            'google_id': partner.google_id,
            'google_name': partner.google_name,
            'google_email': partner.google_email,
            'google_photo': partner.google_photo,
            'rating': partner.rating,
            'state': str(partner.state or 'draft'),
            'is_driver': partner.is_driver,
            'is_active_driver': partner.is_active_driver,
            'identity_file' : partner.identity_file.decode('utf-8') if partner.identity_file else '',
            'license_file' : partner.license_file.decode('utf-8') if partner.license_file else '',
            'document_file' : partner.document_file.decode('utf-8') if partner.document_file else '',
            'vehicle_file' : partner.vehicle_file.decode('utf-8') if partner.vehicle_file else '',
            'assurance_file' : partner.assurance_file.decode('utf-8') if partner.assurance_file else '',
            'is_identity_validated': partner.is_identity_validated,
            'is_license_validated': partner.is_license_validated,
            'is_document_validated': partner.is_document_validated,
            'is_vehicle_validated': partner.is_vehicle_validated,
            'is_assurance_validated': partner.is_assurance_validated,
            'is_verified': partner.is_verified
        }
        
        response = Response(json.dumps(data_response), content_type="application/json", status=200)
        return response
    
    # Update partner by id
    @http.route('/yaawi/api/v1/partner/<int:partner_id>', auth='public', type='http', methods=['PUT'], cors='*', csrf=False)
    def update_partner(self, partner_id, **kw):
        partner = request.env['res.partner'].sudo().browse(partner_id)
        if not partner:
            return Response(json.dumps({
                'error': 'Utilisateur introuvable'
            }))
            
        data = json.loads(request.httprequest.data)
        
        if not data:
            return Response(json.dumps({'success': False, 'error': 'Invalid JSON data'}), content_type='application/json', status=400)

        partner.write({
            'name': data.get('name'),
            'email': data.get('email'),
            'google_id': data.get('google_id'),
            'google_name': data.get('google_name'),
            'google_photo': data.get('google_photo'),
            'google_email': data.get('google_email'),
            'rating': data.get('rating'),
            'state': data.get('state'),
            'is_driver': data.get('is_driver'),
            'is_active_driver': data.get('is_active_driver'),
            'identity_file' : data.get('identity_file'),
            'license_file' : data.get('license_file'),
            'document_file' : data.get('document_file'),
            'vehicle_file' : data.get('vehicle_file'),
            'assurance_file' : data.get('assurance_file'),
            'is_identity_validated': data.get('is_identity_validated'),
            'is_license_validated': data.get('is_license_validated'),
            'is_document_validated': data.get('is_document_validated'),
            'is_vehicle_validated': data.get('is_vehicle_validated'),
            'is_assurance_validated': data.get('is_assurance_validated'),
            'is_verified': data.get('is_verified')
        })
        
        data_response = {
            'success': True,
            'id': partner.id,
            'name': partner.name,
            'email': str(partner.email or ''),
            'google_id': partner.google_id,
            'google_name': partner.google_name,
            'google_email': partner.google_email,
            'google_photo': partner.google_photo,
            'rating': partner.rating,
            'state': str(partner.state or 'draft'),
            'is_driver': partner.is_driver,
            'is_active_driver': partner.is_active_driver,
            'identity_file' : partner.identity_file.decode('utf-8') if partner.identity_file else '',
            'license_file' : partner.license_file.decode('utf-8') if partner.license_file else '',
            'document_file' : partner.document_file.decode('utf-8') if partner.document_file else '',
            'vehicle_file' : partner.vehicle_file.decode('utf-8') if partner.vehicle_file else '',
            'assurance_file' : partner.assurance_file.decode('utf-8') if partner.assurance_file else '',
            'is_identity_validated': partner.is_identity_validated,
            'is_license_validated': partner.is_license_validated,
            'is_document_validated': partner.is_document_validated,
            'is_vehicle_validated': partner.is_vehicle_validated,
            'is_assurance_validated': partner.is_assurance_validated,
            'is_verified': partner.is_verified
        }
        
        response = Response(json.dumps(data_response), content_type="application/json", status=200)
        return response
    
    # Update partner is_active_driver by id
    @http.route('/yaawi/api/v1/partner/<int:partner_id>/active', auth='public', type='http', methods=['PUT'], cors='*', csrf=False)
    def update_partner_is_active_driver(self, partner_id, **kw):
        partner = request.env['res.partner'].sudo().browse(partner_id)
        if not partner:
            return Response(json.dumps({
                'error': 'Utilisateur introuvable'
            }))

        data = json.loads(request.httprequest.data)
        if not data:
            return Response(json.dumps({'success': False, 'error': 'Invalid JSON data'}), content_type='application/json', status=400)
        is_active_driver = data.get('is_active_driver')
        if is_active_driver is None:
            return Response(json.dumps({'success': False, 'error': 'Missing required field'}), content_type='application/json', status=400)
        partner.write({
            'is_active_driver': is_active_driver
        })
        data_response = {
            'success': True,
            'is_active_driver': partner.is_active_driver,
        }
        
        response = Response(json.dumps(data_response), content_type="application/json", status=200)
        return response