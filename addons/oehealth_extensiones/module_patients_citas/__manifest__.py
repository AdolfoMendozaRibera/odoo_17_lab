{
    'name': 'OeHealth Custom Appointments ofitial',
    'version': '17.0.1.0.0',
    'category': 'Healthcare',
    'summary': 'Custom extensions for OeHealth Appointments',
    'description': """
        Este módulo extiende la funcionalidad de citas en OeHealth
        agregando nuevas opciones de estado de paciente
    """,
    'author': 'Ribentek',
    'license': 'LGPL-3',
    'depends': [
        'sale', 
        'oehealth',
        'module_roles_oehealth',
        'oehealth_whatsapp',
        'web', 
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/product_data.xml',
        'data/whatsapp_template_data.xml',
        'views/patient_plan_extend_view.xml',
        'views/patient_appointments_buttons_view.xml',
        'views/appointment_time_extend_view.xml', 
        'views/appointment_view.xml',
        'views/appointment_reprogramar_wizard_view.xml',
        'views/patient_control_service_wizard_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'module_patients_citas/static/src/css/oehealth_calendar_colors.css',
        ],
    },
    'installable': True,
    'auto_install': False,
}