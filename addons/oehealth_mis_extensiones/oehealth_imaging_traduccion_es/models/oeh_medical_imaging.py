from odoo import fields, models

class OeHealthImagingTestDepartment(models.Model):
    _inherit = 'oeh.medical.imagingtest.department'

    name = fields.Char(string='Name', translate=True)

class OeHealthImagingTestType(models.Model):
    _inherit = 'oeh.medical.imaging.test.type'

    name = fields.Char(string='Name', translate=True)

class OeHealthImagingTypeManagement(models.Model):
    _inherit = 'oeh.medical.imaging'

    # Traducimos los campos de texto donde el médico escribe sus hallazgos
    analysis = fields.Text(string='Analysis', translate=True)
    conclusion = fields.Text(string='Conclusion', translate=True)