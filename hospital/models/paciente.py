from odoo import models, fields, api


class hospital(models.Model):
    _name = 'hospital.paciente'
    _description = 'Paciente del hospital'
    
    nombre = fields.Char(
        string='Nombre del paciente',
        required=True,
        help='Nombre completo del paciente'
    )
    
    fecha_nacimiento = fields.Date(
        string='Fecha de Nacimiento',
        help='Fecha de nacimiento del paciente'
    )
    
    fecha_ingreso = fields.Datetime(
        string='Fecha de Ingreso',
        default=fields.Datetime.now,
        help='Fecha y hora de ingreso del paciente'
    )
    
    genero = fields.Selection([
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino'),
        ('otro', 'Otro'),
    ],
        string='Género',
        required=True,
        help='Género del paciente'
    )

