{
    'name': 'Medical Evolution & Protocol Tracking',
    'version': '17.0.1.0.0',
    'category': 'Medical',
    'summary': 'Track patient evolution related to prescriptions/protocols',
    'description': """
        Hu06 Implementation:
        - Link Evaluations to Prescriptions (Protocols).
        - Dashboard/Graph view for patient evolution (Weight, Glucose, Cholesterol, etc.).
        - Compare evolution across time periods.
    """,
    'author': 'Ribentek',
    'depends': ['base', 'oehealth'],
    'data': [
        'views/oeh_medical_evaluation_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
