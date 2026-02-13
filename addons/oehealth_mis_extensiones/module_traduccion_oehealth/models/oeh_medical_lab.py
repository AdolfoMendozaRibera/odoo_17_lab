from odoo import fields, models

# 1. Departamentos de Laboratorio (ej. Bioquímica, Hematología)
class OeHealthLabTestDepartment(models.Model):
    _inherit = 'oeh.medical.labtest.department'

    name = fields.Char(string='Name', translate=True)

# 2. Tipos de Exámenes (ej. Semen Analysis, Hemograma)
class OeHealthLabTestTypes(models.Model):
    _inherit = 'oeh.medical.labtest.types'

    name = fields.Char(string='Lab Test Name', translate=True)
    info = fields.Text(string='Description', translate=True)

# 3. Criterios/Parámetros del Examen (ej. Viscosity, Normal Range)
class OeHealthLabTestCriteria(models.Model):
    _inherit = 'oeh.medical.labtest.criteria'

    name = fields.Char(string='Tests', translate=True)
    normal_range = fields.Text(string='Normal Range', translate=True)

# 4. Unidades de Medida de Laboratorio
class OeHealthLabUnits(models.Model):
    _inherit = 'oeh.medical.lab.units'

    name = fields.Char(string='Name', translate=True)

# 5. Tipos de Muestra de Laboratorio (ej. Sangre, Orina, Lavado Gástrico)
class OeHealthSampleType(models.Model):
    _inherit = "oeh.medical.sample.types"

    name = fields.Char(string='Sample Types', translate=True)