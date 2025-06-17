from odoo import models, fields

class Clase(models.Model):
    _name = 'gestion_cursos.clase'
    _description = 'Clase'

    name = fields.Char(string='Tema o Título', required=True)
    curso_id = fields.Many2one('gestion_cursos.curso', string='Curso', required=True)
    fecha = fields.Datetime(string='Fecha y Hora de la clase')
    fecha_fin = fields.Datetime(string='Fecha y Hora de Fin de la clase')
    duracion_minutos = fields.Integer(string='Duración (minutos)')
