from odoo import fields, models

class OeHealthIC10Procedures(models.Model):
    _inherit = 'oeh.medical.procedure'

    # El 'name' es el código numérico, no se traduce.
    # La 'description' es el texto médico, este SÍ se traduce.
    description = fields.Char(string='Long Text', translate=True)