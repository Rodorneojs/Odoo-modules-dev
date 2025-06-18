# -*- coding: utf-8 -*-
from odoo import models, fields, api

class InscribirAlumnosWizard(models.TransientModel):
    _name = 'gestion_cursos.inscribir_alumnos_wizard'
    _description = 'Wizard para inscribir alumnos a un curso'

    curso_id = fields.Many2one('gestion_cursos.curso', string='Curso', required=True)
    alumno_ids = fields.Many2many('gestion_cursos.alumno',relation='wizard_alumno_rel', string='Alumnos', required=True)

    def action_inscribir(self):
        # Método para crear inscripciones en base a la selección
        inscripcion_obj = self.env['gestion_cursos.inscripcion']
        template = self.env.ref('gestion_cursos.email_template_inscripcion_curso')
        if not template:
            raise ValueError("No se encontró la plantilla de email para inscripciones.")    

        for alumno in self.alumno_ids:
            inscripcion = inscripcion_obj.create({
                'curso_id': self.curso_id.id, 
                'alumno_id': alumno.id,
            })
            # Enviar email con plantilla
            template.send_mail(inscripcion.id, force_send=True)
        return {'type': 'ir.actions.act_window_close'}  # Cierra el wizard
