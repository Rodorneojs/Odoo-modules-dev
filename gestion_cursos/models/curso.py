from odoo import models, fields

class Curso(models.Model):
    _name = 'gestion_cursos.curso'
    _description = 'Curso'

    name = fields.Char(string='Nombre del Curso', required=True)
    descripcion = fields.Text(string='Descripción')
    fecha_inicio = fields.Date(string='Fecha de Inicio')
    fecha_fin = fields.Date(string='Fecha de Fin')
    duracion_horas = fields.Integer(string='Duración (horas)')
