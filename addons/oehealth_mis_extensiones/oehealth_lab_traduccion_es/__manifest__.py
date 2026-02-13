{
    'name': 'oeHealth - Traduccion - Laboratory Information System',
    'version': '17.0.1.0.0',
    'category': 'Localization',
    'summary': 'Traducción al español para el módulo oeHealth laboratory',
    'author': 'Adolfo-Ribentek',
    'depends': [
        'oehealth',
        'oehealth_lab',
    ],
    'data': [
        #'i18n/es.po',
        'views/oeh_medical_view_es.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}