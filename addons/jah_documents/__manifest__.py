{
    'name': 'JAH-Mejoras Documentos de Venta',
    'version': '17.0.1.0.0',
    'category': 'Sales',
    'summary': 'Personalización de documentos de venta para JAH',
    'description': """
        Módulo de personalización de documentos de venta para JAH
        =========================================================
        
        Características:
        ----------------
        * Encabezado unificado corporativo
        * Tablas ajustadas con columna de descuento visible
        * Estructura de cliente estandarizada
        * Firmas en órdenes de venta
        * Ocultar campos fiscales en cotizaciones
        * Mantiene funcionalidad nativa de Odoo
        
    """,
    'author': 'JAH Adolfo',
    'website': 'https://jah.com',
    'depends': [
        'base',
        'sale',
        'sale_management',
        'web',
    ],
    'data': [
        'reports/report_jah_saleorder_document.xml',
    ],
    
    """
    'assets': {
        'web.report_assets_common': [
            'jah_sale_documents/static/src/css/report_styles.css',
        ],
    },
    """
    
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}