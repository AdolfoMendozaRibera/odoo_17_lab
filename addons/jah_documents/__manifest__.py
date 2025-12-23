{
    'name': 'JAH-Mejoras Documentos de Venta 2',
    'version': '17.0.1.0.0',
    'category': 'Sales',
    'summary': 'Personalización de documentos de venta para JAH',
    'description': """...""",
    'author': 'JAH Adolfo',
    'website': 'https://jah.com',
    'depends': [
        'base',
        'web',
        'account',
        'sale',
        'sale_management',
    ],
    'data': [
        'reports/jah_common_header_report.xml',
        'reports/jah_common_footer_report.xml',
        'reports/jah_saleorder_document_report.xml',
        'reports/jah_account_document_report.xml',
        'reports/jah_stock_document_report.xml',
    ],
    'assets': {
        'web.report_assets_common': [
            'jah_documents/static/src/scss/jah_header_style.scss',
            'jah_documents/static/src/scss/jah_footer_style.scss',
            'jah_documents/static/src/scss/jah_common_styles.scss',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}