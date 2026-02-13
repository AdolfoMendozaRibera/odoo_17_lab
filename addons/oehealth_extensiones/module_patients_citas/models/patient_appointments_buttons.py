from odoo import models, api

class OeHealthPatientAppointmentButtons(models.Model):

    _inherit = 'oeh.medical.patient'

    # ========================== METODOS PARA LOS BOTONES DE CITAS ==========================
    def action_view_medicion_appointments(self):
        """Abre las citas de MEDICIÓN de este paciente"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Citas - Medición: {self.firstname} {self.lastname}',
            'res_model': 'oeh.medical.appointment',
            'view_mode': 'calendar,tree,form',
            'domain': [
                ('patient', '=', self.id),
                ('appointment_type', '=', 'Medición')
            ],
            'context': {'default_patient': self.id},  # ← SIN default_appointment_type
            'target': 'current',
        }
    
    def action_view_control_appointments(self):
        """Abre las citas de CONTROL de este paciente"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Citas - Control: {self.firstname} {self.lastname}',
            'res_model': 'oeh.medical.appointment',
            'view_mode': 'calendar,tree,form',
            'domain': [
                ('patient', '=', self.id),
                ('appointment_type', '=', 'Control')
            ],
            'context': {'default_patient': self.id},  # ← SIN default_appointment_type
            'target': 'current',
        }
    
    def action_view_control_medicion_appointments(self):
        """Abre las citas de CONTROL MEDICIÓN de este paciente"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Citas - Control Medición: {self.firstname} {self.lastname}',
            'res_model': 'oeh.medical.appointment',
            'view_mode': 'calendar,tree,form',
            'domain': [
                ('patient', '=', self.id),
                ('appointment_type', '=', 'Control Medición')
            ],
            'context': {'default_patient': self.id},  # ← SIN default_appointment_type
            'target': 'current',
        }
    
    def action_view_suero_appointments(self):
        """Abre las citas de SUERO de este paciente"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Citas - Suero: {self.firstname} {self.lastname}',
            'res_model': 'oeh.medical.appointment',
            'view_mode': 'calendar,tree,form',
            'domain': [
                ('patient', '=', self.id),
                ('appointment_type', '=', 'Suero')
            ],
            'context': {'default_patient': self.id},  # ← SIN default_appointment_type
            'target': 'current',
        }
    
    def action_view_inyectable_appointments(self):
        """Abre las citas de INYECTABLE de este paciente"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Citas - Inyectable: {self.firstname} {self.lastname}',
            'res_model': 'oeh.medical.appointment',
            'view_mode': 'calendar,tree,form',
            'domain': [
                ('patient', '=', self.id),
                ('appointment_type', '=', 'Inyectable')
            ],
            'context': {'default_patient': self.id},  # ← SIN default_appointment_type
            'target': 'current',
        }