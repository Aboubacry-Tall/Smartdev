# -*- coding: utf-8 -*-
# from odoo import http


# class SmartPayroll(http.Controller):
#     @http.route('/smart_payroll/smart_payroll', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/smart_payroll/smart_payroll/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('smart_payroll.listing', {
#             'root': '/smart_payroll/smart_payroll',
#             'objects': http.request.env['smart_payroll.smart_payroll'].search([]),
#         })

#     @http.route('/smart_payroll/smart_payroll/objects/<model("smart_payroll.smart_payroll"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('smart_payroll.object', {
#             'object': obj
#         })

