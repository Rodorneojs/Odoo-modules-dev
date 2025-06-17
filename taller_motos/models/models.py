# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.convert import ValidationError
from odoo.exceptions import ValidationError

class Moto(models.Model):
    _name = 'taller.moto'
    _description = 'Moto'
    _sql_constraints = [
    ('placa_unica', 'unique(name)', 'La placa ya está registrada. Debe ser única.')
    ]


    name = fields.Char(string='Placa', required=True)
    marca = fields.Char(string='Marca')
    modelo = fields.Char(string='Modelo')
    color = fields.Char(string='Color')
    anio = fields.Integer(string='Año')

    # Computed field to generate a description based on marca, modelo, and name
    descripcion = fields.Text(
        string='Descripción',
        compute='_compute_descripcion',
        store=True
         # opcional si quieres permitir edición manual además
    )
    # Campo computado para contar la cantidad de trabajos realizados en la moto
    cantidad_trabajos = fields.Integer(
    string='Cantidad de Trabajos',
    compute='_compute_cantidad_trabajos',
    store=True
    )
    # Campo computado para mostrar el último estado de trabajo
    ultimo_estado_trabajo = fields.Selection(
    string='Último Estado de Trabajo',
    selection=[
        ('pendiente', 'Pendiente'),
        ('proceso', 'En Proceso'),
        ('terminado', 'Terminado')
    ],
    compute='_compute_ultimo_estado_trabajo',
    store=True
    )

    # Campo para contar los trabajos terminados
    trabajos_terminados = fields.Integer(
    string='Trabajos Terminados',
    compute='_compute_trabajos_terminados',
    store=True
    )


    fecha_ingreso = fields.Date(string='Fecha de Ingreso')
    cliente_id = fields.Many2one('taller.cliente', string='Cliente')
    trabajo_ids = fields.One2many('taller.trabajo', 'moto_id', string='Trabajos realizados')
    telefono_cliente = fields.Char(string="Teléfono del Cliente", readonly=True)

    @api.onchange('cliente_id')
    def _onchange_cliente_id(self):
        if self.cliente_id:
            self.telefono_cliente = self.cliente_id.telefono
        else:
            self.telefono_cliente = False

    @api.depends('name', 'marca', 'modelo', 'color', 'anio')
    def _compute_descripcion(self):
        for moto in self:
            print(f"Computando descripción para: {moto.name}")
            partes = []
            if moto.marca:
                partes.append(moto.marca)
            if moto.modelo:
                partes.append(moto.modelo)
            if moto.color:
                partes.append(f"de color {moto.color}")
            if moto.anio:
                partes.append(f"(Año: {moto.anio})")
            if moto.name:
                partes.append(f"- Placa: {moto.name}")
            moto.descripcion = "Moto " + " ".join(partes)

    @api.constrains('name')
    def _check_placa_unica(self):
        for record in self:
            existing = self.search([('name', '=', record.name), ('id', '!=', record.id)], limit=1)
            if existing:
                raise ValidationError('Ya existe una moto registrada con esa placa.')
    # Este método se asegura de que la placa sea única en el sistema.
    # Si intentas registrar una moto con una placa que ya existe, Odoo te mostrará un error de validación y no te permitirá guardar el registro.
    # Además, se asegura de que la placa no esté registrada a nombre de otro cliente.
    @api.constrains('name', 'cliente_id')
    def _check_placa_cliente_unico(self):
        for record in self:
            if record.name and record.cliente_id:
                existe = self.env['taller.moto'].search([
                    ('name', '=', record.name),
                    ('cliente_id', '!=', record.cliente_id.id),
                    ('id', '!=', record.id)
                ])
                if existe:
                    raise ValidationError(
                        f"La moto con placa '{record.name}' ya está registrada a nombre de otro cliente."
                    )
                
    # Metodo para calcular la cantidad de trabajos realizados en la moto
    # Este método se ejecuta automáticamente cada vez que se crea, actualiza o elimina un trabajo relacionado con la moto.
    # Actualiza el campo `cantidad_trabajos` con el número de trabajos asociados a la moto.
    @api.depends('trabajo_ids')
    def _compute_cantidad_trabajos(self):
        for record in self:
            record.cantidad_trabajos = len(record.trabajo_ids)

    # Método para calcular el último estado de trabajo
    # Este método busca el trabajo más reciente basado en la fecha y actualiza el campo `
    @api.depends('trabajo_ids.fecha', 'trabajo_ids.estado')
    def _compute_ultimo_estado_trabajo(self):
        for record in self:
            if record.trabajo_ids:
                trabajo_mas_reciente = max(record.trabajo_ids, key=lambda t: t.fecha or fields.Date.today())
                record.ultimo_estado_trabajo = trabajo_mas_reciente.estado
            else:
                record.ultimo_estado_trabajo = False
    def action_ver_trabajos(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Trabajos de la Moto',
            'view_mode': 'list,form',
            'res_model': 'taller.trabajo',
            'domain': [('moto_id', '=', self.id)],
            'context': {'default_moto_id': self.id},
        }
    @api.depends('trabajo_ids.estado')
    def _compute_trabajos_terminados(self):
        for record in self:
            terminados = record.trabajo_ids.filtered(lambda t: t.estado == 'terminado')
            record.trabajos_terminados = len(terminados)
    def action_ver_trabajos(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Trabajos de esta Moto',
            'view_mode': 'list,form',
            'res_model': 'taller.trabajo',
            'domain': [('moto_id', '=', self.id)],
            'context': {'default_moto_id': self.id},
        }

class Trabajo(models.Model):
    _name = 'taller.trabajo'
    _description = 'Trabajo realizado en una moto'

    name = fields.Char(string="Nombre del Trabajo", required=True)
    fecha = fields.Date(string="Fecha", required=True)
    costo = fields.Float(string="Costo")
    estado = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('proceso', 'En proceso'),
        ('terminado', 'Terminado')
    ], string="Estado", default='pendiente')
    observaciones = fields.Text(string="Observaciones")
    moto_id = fields.Many2one('taller.moto', string="Moto", required=True)
    mecanico_id = fields.Many2one('taller.mecanico', string='Mecánico asignado')


class Mecanico(models.Model):
    _name = 'taller.mecanico'
    _description = 'Mecánico'

    name = fields.Char(string='Nombre', required=True)
    telefono = fields.Char(string='Teléfono')
    especialidad = fields.Char(string='Especialidad')
    trabajo_ids = fields.One2many('taller.trabajo', 'mecanico_id', string='Trabajos asignados')

class Cliente(models.Model):
    _name = 'taller.cliente'
    _description = 'Cliente del Taller'

    name = fields.Char(string='Nombre completo', required=True)
    ci = fields.Char(string='Cédula de identidad')
    telefono = fields.Char(string='Teléfono')
    email = fields.Char(string='Correo electrónico')
    direccion = fields.Text(string='Dirección')
    moto_ids = fields.One2many('taller.moto', 'cliente_id', string='Motos')