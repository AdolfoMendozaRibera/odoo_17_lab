{
    'name': 'Module Nurses',
    'version': '17.0.1.0.0',
    'summary': 'Control de pacientes atendidos por enfermeras y registro de Insumos',
    'description': """
        Historia de Usuario HU07:
        - Contador de pacientes atendidos por enfermera.
        - Visualización en Kanban y Tree view de enfermeras.
        - Filtro por periodo de tiempo (día, semana, mes, año).
    """,
    'category': 'Medical',
    'author': 'Ribentek',
    'depends': ['base', 'oehealth', 'stock'],
     'data': [
        'security/ir.model.access.csv', 
        'views/nurses_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
