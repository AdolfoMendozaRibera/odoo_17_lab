from odoo import fields, models, api, _


class PatientControlServiceWizard(models.TransientModel):
    _name = 'patient.control.service.wizard'
    _description = 'Wizard para seleccionar tipo de servicio'

    SERVICE_TYPES = [
        ('medicion', '📏 Plan de Medición'),
        ('ortomolecular', '💉 Plan Ortomolecular'),
        ('completo', '⭐ Plan Completo WB'),
    ]

    service_type = fields.Selection(
        selection=SERVICE_TYPES,
        string='Tipo de Servicio',
        required=True,
        help='Selecciona el tipo de servicio que desea agendar'
    )

    patient_id = fields.Many2one(
        'oeh.medical.patient',
        string='Paciente',
        readonly=True,
        help='Paciente para el cual se crea la cita'
    )

    def action_confirm(self):
        """Abrir formulario de paciente con el plan preseleccionado"""
        self.ensure_one()
        
        # Abrir formulario de paciente nuevo con el plan preseleccionado
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'oeh.medical.patient',
            'view_mode': 'form',
            'views': [[False, 'form']],
            'target': 'current',
            'context': {
                'default_service_plan': self.service_type
            }
        }
