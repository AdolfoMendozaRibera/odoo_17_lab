{
    'name': 'JAH - Documentos de Stock',
    'version': '17.0.1.0.0',
    'category': 'Inventory',
    'summary': 'Nota de entrega personalizada para JAH',
    'description': """
        Nota de entrega JAH con:
        - Tabla sin precios
        - Columnas: Código, Descripción, Unidad, Ordenado, Entregado
        - Firmas de responsable y cliente
    """,
    'author': 'JAH',
    'website': 'https://jah.com',
    'depends': ['stock'],  # Solo depende de stock
    'data': [
        'reports/stock_reports.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}