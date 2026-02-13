from odoo import http
from  odoo.http import request
import json

class PatientControlController(http.Controller):

    @http.route('/patient_control/get_service_types', type='json', auth='user')
    def get_service_types(self):
        """
        Retorna los tipos de servicios disponibles para el serrvicio
        """
        service_types = [
            {
                'id': 'medicion',
                'name': 'Plan de Medición',
                'icon': '📏',
                'description': 'Solo medición corporal con especialista'
            },
            {
                'id': 'ortomolecular',
                'name': 'Plan Ortomolecular',
                'icon': '💉',
                'description': 'Consulta + Protocolo de Sueros'
            },
            {
                'id': 'completo',
                'name': 'Plan Completo WB',
                'icon': '⭐',
                'description': 'Medición + Nutrición + Ortomolecular + 6 Controles (8 citas totales)'
            }
        ]
        return {
            'success':True,
            'service_types':service_types
        }

    @http.route('/patient_control/create_appointment', type='json', auth='user', method='POST')
    def create_appointment(self, **kwargs):
        """
        Crear cita según el tipo de servicio seleccionado 
        """
        try: 
            service_type = kwargs.get('service_type')
            patient_id = kwargs.get('patient_id')

            # Aquí iría la lógica para crear la cita
            # Por ahora solo retornamos que fue exitoso

            return {
                'success':True,
                'message':f'Cita creada con éxito para el servicio {service_type}',
                'service_type':service_type
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    @http.route('/patient_control/create_patient_with_plan', type='json', auth='user', method='POST')
    def create_patient_with_plan(self, **kwargs):
        """Crear nuevo paciente con plan preseleccionado"""
        try:
            service_plan = kwargs.get('service_plan')
            
            # Aquí Odoo abrirá el formulario del paciente con el plan preseleccionado
            return {
                'success': True,
                'service_plan': service_plan,
                'action': 'create_patient'
            }

        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }