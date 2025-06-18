from odoo import models, fields

class Docente(models.Model):
    _name = 'gestion_cursos.docente'
    _inherits = {'res.partner': 'partner_id'}
    _description = 'Docente'

    partner_id = fields.Many2one('res.partner', required=True, ondelete='cascade')
    titulo = fields.Char(string="Título Académico")
    experiencia = fields.Integer(string="Años de experiencia")
