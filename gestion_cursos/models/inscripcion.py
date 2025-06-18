from odoo import models, fields, api

class Inscripcion(models.Model):
    _name = 'gestion_cursos.inscripcion'
    _description = 'Inscripción de Alumno a Curso'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    alumno_id = fields.Many2one('gestion_cursos.alumno', string='Alumno', required=True)
    curso_id = fields.Many2one('gestion_cursos.curso', string='Curso', required=True)
    fecha_inscripcion = fields.Date(string='Fecha de Inscripción', default=fields.Date.context_today)
    estado = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
    ], string='Estado', default='pendiente')
