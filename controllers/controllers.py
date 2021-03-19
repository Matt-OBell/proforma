# -*- coding: utf-8 -*-
from odoo import http

# class Pro-forma(http.Controller):
#     @http.route('/pro-forma/pro-forma/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pro-forma/pro-forma/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pro-forma.listing', {
#             'root': '/pro-forma/pro-forma',
#             'objects': http.request.env['pro-forma.pro-forma'].search([]),
#         })

#     @http.route('/pro-forma/pro-forma/objects/<model("pro-forma.pro-forma"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pro-forma.object', {
#             'object': obj
#         })