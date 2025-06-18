from odoo import models, fields

class Alumno(models.Model):
    _name = 'gestion_cursos.alumno'
    _description = 'Alumno'

    name = fields.Char(string='Nombre Completo', required=True)
    email = fields.Char(string='Correo Electrónico')
    telefono = fields.Char(string='Teléfono')
    curso_ids = fields.Many2many('gestion_cursos.curso', string='Cursos Inscritos', relation='alumno_curso_rel')
    user_id = fields.Many2one('res.users', string='Usuario relacionado')
