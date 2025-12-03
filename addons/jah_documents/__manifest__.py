{
    'name': 'JAH-Mejoras Documentos de Venta 2',
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
        'account',
        'sale',
        'sale_management',
        'web',
    ],
    'data': [
        #'reports/report_jah_external_layout.xml',
        #'reports/report_jah_common_header.xml',
        'reports/report_jah_external_layout.xml',
        'reports/report_jah_saleorder_document.xml',
        'reports/report_jah_account_document.xml',
        #'reports/report_jah_stock_document.xml',
    ],
   
    #'assets': {
    #    'web.report_assets_common': [
    #        'jah_sale_documents/static/src/css/report_styles.css',
    #    ],
    
    
    #'assets': {
    #    'web.report_assets_common': [
    #        'jah_sale_documents/static/src/css/jah_reports.css',
    #    ],
    #},
    
    
    
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}