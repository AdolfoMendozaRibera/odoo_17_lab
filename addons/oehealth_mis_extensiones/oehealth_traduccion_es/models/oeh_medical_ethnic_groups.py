from odoo import fields, models

class OeHealthEthnicGroups(models.Model):
    _inherit = 'oeh.medical.ethnicity' # Heredamos el modelo original

    # Redefinimos el campo solo para agregar el atributo translate=True
    name = fields.Char(string='Ethnic Groups', translate=True)