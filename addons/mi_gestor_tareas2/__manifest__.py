# -*- coding: utf-8 -*-
{
    # Nombre del módulo (lo que aparecerá en la lista de aplicaciones)
    'name': 'Gestor de Tareas',
    
    # Versión del módulo (formato: versión_odoo.versión_módulo)
    'version': '17.0.1.0.0',
    
    # Categoría donde aparecerá el módulo en la lista de aplicaciones
    'category': 'Productivity',
    
    # Descripción corta que aparece en la lista de módulos
    'summary': 'Sistema completo de gestión de tareas con categorías y etiquetas',
    
    # Autor del módulo
    'author': 'Adolfo',
    
    # Sitio web (opcional)
    'website': 'https://www.tuempresa.com',
    
    # Licencia del módulo (LGPL-3 es la más común en Odoo)
    'license': 'LGPL-3',
    
    # Módulos de los que depende este módulo
    # 'base' es obligatorio porque contiene modelos básicos como res.partner
    # 'mail' es para herencia de funcionalidades de mensajería
    'depends': ['base', 'mail'],
    
    # Archivos de datos que se cargarán en orden
    'data': [
        # Primero la seguridad (permisos de acceso)
        'security/ir.model.access.csv',
        
        # Luego las vistas
        'views/categoria_views.xml',
        'views/etiqueta_views.xml',
        'views/tarea_views.xml',
        
        # Acciones especiales
        'data/acciones.xml',
        
        # Reportes
        'report/reporte_tarea.xml',
    ],
    
    # Archivos de demostración (datos de prueba)
    # Se cargan solo si instalas el módulo con data de demo
    'demo': [],
    
    # Archivos QWeb para web/portal
    'assets': {
        'web.assets_backend': [],
    },
    
    # ¿Se puede instalar directamente desde la UI?
    'installable': True,
    
    # ¿Es una aplicación o un módulo técnico?
    # True = aparece como app en el menú principal
    'application': True,
    
    # ¿Se instala automáticamente con Odoo? (casi nunca True)
    'auto_install': False,
}