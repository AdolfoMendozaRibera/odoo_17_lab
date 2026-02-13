{
    'name': 'Roles Personalizados oeHealth Ribentek',
    'version': '17.0.1.0.0',
    'category': 'Medical',
    'summary': 'Agrega roles de Recepción y Farmacia al módulo oeHealth',
    'description': """
        Este módulo extiende oeHealth para agregar roles específicos requeridos por el centro de nutrición:
        - Recepción / Admisión
        - Farmacia / Almacén
    """,
    'author': 'Ribentek',
    'depends': ['oehealth'],
    'data': [
        'security/res_groups.xml',    
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
