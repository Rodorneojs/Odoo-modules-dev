# -*- coding: utf-8 -*-
# from odoo import http


# class TallerMotos(http.Controller):
#     @http.route('/taller_motos/taller_motos', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/taller_motos/taller_motos/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('taller_motos.listing', {
#             'root': '/taller_motos/taller_motos',
#             'objects': http.request.env['taller_motos.taller_motos'].search([]),
#         })

#     @http.route('/taller_motos/taller_motos/objects/<model("taller_motos.taller_motos"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('taller_motos.object', {
#             'object': obj
#         })

