from odoo import fields, models

class OeHealthSurgery(models.Model):
    _inherit = "oeh.medical.surgery"

    # Habilitamos traducción para campos de texto
    description = fields.Text(string='Description', translate=True)
    info = fields.Text(string='Extra Info', translate=True)
    anesthesia_report = fields.Text(string='Anesthesia Report', translate=True)