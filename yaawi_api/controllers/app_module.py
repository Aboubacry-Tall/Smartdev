# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request, Response
import json


class ModuleController(http.Controller):

    #Get ride modules
    @http.route('/yaawi/api/v1/modules', auth='public', type='http', methods=['GET'], cors='*', csrf=False)
    def get_all_services(self, **kw):
        services = request.env['app.module'].sudo().search([])
        
        data_response = [{
            'success': True,
            'id': service.id,
            'name': service.name,
            'state': service.state,
        } for service in services]
        
        response = Response(json.dumps(data_response), content_type="application/json", status=200)
        return response