from odoo import fields, models

class OeHealthGenetics(models.Model):
    _inherit = 'oeh.medical.genetics'

    name = fields.Char(string='Official Symbol', translate=True)
    long_name = fields.Char(string='Official Long Name', translate=True)
    info = fields.Text(string='Information', translate=True)