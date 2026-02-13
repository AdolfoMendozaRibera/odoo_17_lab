from odoo import fields, models

# 1. Para las ocupaciones (Maestro)
class OeHealthOccupations(models.Model):
    _inherit = "oeh.medical.occupation"

    name = fields.Char(string='Occupation', translate=True)

# 2. Para los datos socioeconómicos (Extensión del Paciente)
class OehMedicalPatient(models.Model):
    _inherit = 'oeh.medical.patient'

    # Traducimos el campo de texto libre
    info = fields.Text(string="Extra info", translate=True)
    
    # Nota: Los campos Selection (socioeconomics, education_level, etc.) 
    # NO necesitan translate=True en Python, se traducen directamente en el .po