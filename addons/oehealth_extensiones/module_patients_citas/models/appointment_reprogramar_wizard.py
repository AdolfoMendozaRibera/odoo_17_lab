from odoo import fields, models, api, _
from odoo.exceptions import UserError
from datetime import datetime


class AppointmentReprogramarWizard(models.TransientModel):

    _name = 'appointment.reprogramar.wizard'
    _description = 'Wizard para Reprogramar Citas'

    appointment_id = fields.Many2one(
        'oeh.medical.appointment',
        string='Cita Original',
        readonly=True
    )
    
    new_appointment_date = fields.Datetime(
        string='Nueva Fecha y Hora',
        required=True,
        help='Selecciona la nueva fecha y hora para la cita'
    )
    
    notes = fields.Text(
        string='Notas',
        help='Notas adicionales sobre la reprogramación'
    )

    @api.onchange('new_appointment_date')
    def _onchange_appointment_date(self):
        """Validar que la nueva fecha sea en el futuro"""
        if self.new_appointment_date:
            if self.new_appointment_date <= datetime.now():
                return {
                    'warning': {
                        'title': _('Fecha Inválida'),
                        'message': _('La nueva fecha debe ser en el futuro'),
                    }
                }

    def action_reprogramar(self):
        """
        Ejecutar la reprogramación:
        1. Marcar la cita original como 'Reprogramada'
        2. Crear duplicado con estado 'Programada' y nueva fecha
        """
        self.ensure_one()
        
        if not self.appointment_id:
            raise UserError(_('No se encontró la cita original'))
        
        if not self.new_appointment_date:
            raise UserError(_('Debes seleccionar una nueva fecha y hora'))
        
        # Validación adicional de fecha
        if self.new_appointment_date <= datetime.now():
            raise UserError(_('La nueva fecha debe ser en el futuro'))
        
        appointment = self.appointment_id
        
        # Delegar la lógica al modelo de la cita para mantener consistencia
        new_appointment = appointment.create_duplicate_appointment(self.new_appointment_date, self.notes)
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Cita Reprogramada'),
                'message': _('La cita ha sido reprogramada exitosamente.\nCita Original: %s (Reprogramada)\nNueva Cita: %s (Programada)') % (appointment.name, new_appointment.name),
                'type': 'success',
                'sticky': False,
            }
        }