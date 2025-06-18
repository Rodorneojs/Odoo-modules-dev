from odoo import http
from odoo.http import request

class CursoDashboard(http.Controller):
    @http.route('/gestion_cursos/dashboard', type='http', auth='public', website=True)
    def curso_dashboard(self):
        total = request.env['gestion_cursos.curso'].search_count([])
        activos = request.env['gestion_cursos.curso'].search_count([('activo', '=', True)])
        curso_largo = request.env['gestion_cursos.curso'].search([], order='duracion_horas desc', limit=1)
        return request.render('gestion_cursos.curso_dashboard_template', {
            'total_cursos': total,
            'cursos_activos': activos,
            'curso_mas_largo': curso_largo.name if curso_largo else 'N/A',
            'duracion_mas_larga': curso_largo.duracion_horas if curso_largo else 0,
        })
