from odoo import fields, models

class OeHealthRecreationalDrug(models.Model):
    _inherit = "oeh.medical.recreational.drugs"

    # Habilitamos traducción para los nombres y descripciones
    name = fields.Char(string='Drug Name', translate=True)
    street_name = fields.Char(string='Street Names', translate=True)
    info = fields.Text(string='Extra Info', translate=True)