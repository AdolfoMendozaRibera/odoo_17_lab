from odoo import models, fields, api

class OeHealthPatientPlanExtend(models.Model):
    _inherit = 'oeh.medical.patient'

    #Campo para almacenar el plan seleccinado
    service_plan = fields.Selection(
        [
            ('medicion', 'Plan de Medición'),
            ('ortomolecular', 'Plan Ortomolecular'),
            ('completo', 'Plan Completo WB'),
        ],
        string='Tipo de Servicio',
        help='Plan seleccionado para el paciente'
    )