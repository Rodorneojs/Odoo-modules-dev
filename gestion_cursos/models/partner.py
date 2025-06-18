from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    es_docente = fields.Boolean(string="¿Es docente?")
    especialidad = fields.Char(string="Especialidad")
