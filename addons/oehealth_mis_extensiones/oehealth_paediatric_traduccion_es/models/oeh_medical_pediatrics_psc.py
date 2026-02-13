from odoo import fields, models

class OeHealthPediatricSymptomsChecklist(models.Model):
    _inherit = "oeh.medical.pediatrics.psc"

    # Traducimos las notas
    notes = fields.Text(string='Notes', translate=True)

    # Nota técnica: Los campos 'Selection' (psc_aches_pains, etc.) 
    # se traducen mediante el archivo .po, no necesitas re-declararlos aquí.
    # Solo re-declaramos si quisiéramos cambiar el texto del String (la etiqueta).