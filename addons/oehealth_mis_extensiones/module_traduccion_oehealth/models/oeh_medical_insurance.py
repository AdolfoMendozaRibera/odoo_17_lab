from odoo import fields, models

class OeHealthInsuranceType(models.Model):
    _inherit = 'oeh.medical.insurance.type'

    name = fields.Char(translate=True)