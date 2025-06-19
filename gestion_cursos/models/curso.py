from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from datetime import date

class Curso(models.Model):
    _name = 'gestion_cursos.curso'
    _description = 'Curso'

    name = fields.Char(string='Nombre del Curso', required=True)
    descripcion = fields.Text(string='Descripción')
    fecha_inicio = fields.Date(string='Fecha de Inicio')
    fecha_fin = fields.Date(string='Fecha de Fin')
    duracion_horas = fields.Integer(string='Duración (horas)')
    duracion_minutos = fields.Integer(string='Duración (minutos)', required=True)

    clase_count = fields.Integer(string='Nro. de Clases', compute='_compute_clase_count', store=True)
    clase_ids = fields.One2many('gestion_cursos.clase', 'curso_id', string='Clases')
    alumnos_ids = fields.Many2many('gestion_cursos.alumno', string='Alumnos inscritos')
    docente_id = fields.Many2one('gestion_cursos.docente', string='Docente')

    activo = fields.Boolean(string='Activo', default=True)



    @api.depends('clase_ids')
    def _compute_clase_count(self):
        for record in self:
            record.clase_count = len(record.clase_ids)

    def action_ver_clases(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Clases',
            'res_model': 'gestion_cursos.clase',
            'domain': [('curso_id', '=', self.id)],
            'view_mode': 'list,form,calendar',
            'target': 'current',
        }
    def action_inscribirse(self):
        alumno = self.env['gestion_cursos.alumno'].search([('user_id', '=', self.env.uid)], limit=1)
        if not alumno:
            raise UserError("No se encontró un alumno relacionado a este usuario.")
        self.alumnos_ids |= alumno
        return True
    def action_view_details(self):
        raise UserError("Este es un ejemplo. Aquí podrías mostrar un wizard, redireccionar a otra vista, etc.")
    
    @api.constrains('fecha_inicio', 'fecha_fin')
    def _check_fechas_validas(self):
        hoy = date.today()
        for curso in self:
            if curso.fecha_inicio < hoy:
                raise ValidationError("📅 La fecha de inicio no puede estar en el pasado.")
            if curso.fecha_fin < hoy:
                raise ValidationError("📅 La fecha de fin no puede estar en el pasado.")
            if curso.fecha_fin < curso.fecha_inicio:
                raise ValidationError("⚠️ La fecha de fin no puede ser anterior a la fecha de inicio.")