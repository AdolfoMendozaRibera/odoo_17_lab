# -*- coding: utf-8 -*-

{
    # Nombre del módulo (aparecerá en la lista de Apps)
    'name': 'Mi Gestor de Tareas',
    
    # Versión del módulo
    'version': '17.0.1.0.0',
    
    # Descripción corta
    'summary': 'Módulo simple para gestionar tareas personales',
    
    # Descripción detallada
    'description': """
        Este es un módulo de ejemplo para aprender Odoo.
        Permite crear y gestionar tareas simples con:
        - Nombre de la tarea
        - Descripción
        - Estado (pendiente/completada)
        - Fecha límite
    """,
    
    # Autor del módulo
    'author': 'Tu Nombre',
    
    # Categoría donde aparecerá en Apps
    'category': 'Productivity',
    
    # Versión de Odoo compatible
    'depends': ['base'],  # 'base' es el módulo básico de Odoo (siempre necesario)
    
    # Archivos de datos que se cargarán (en orden)
    'data': [
        'security/ir.model.access.csv',  # Permisos de acceso
        'views/tarea_views.xml',         # Vistas (formularios, listas, etc)
    ],
    
    # Si es True, el módulo se instala automáticamente
    'installable': True,
    
    # Si es True, se instala al crear una nueva base de datos
    'auto_install': False,
    
    # Si es True, aparece como App principal, si False como módulo técnico
    'application': True,
    
    # Licencia del módulo
    'license': 'LGPL-3',
}