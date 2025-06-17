from odoo import models, fields

class Evaluacion(models.Model):
    _name = 'gestion_cursos.evaluacion'
    _description = 'Evaluación de Alumno'

    alumno_id = fields.Many2one('gestion_cursos.alumno', string='Alumno', required=True)
    curso_id = fields.Many2one('gestion_cursos.curso', string='Curso', required=True)
    nota = fields.Float(string='Nota')
    comentarios = fields.Text(string='Comentarios')
