from odoo import fields, models

class OeHealthDosage (models.Model):
    _inherit = 'oeh.medical.dosage'

    name = fields.Char(string='Frequency', translate=True, help='Common dosage frequency')
    abbreviation = fields.Char(translate=True)


class OeHealthDoseUnit(models.Model):
    _inherit = 'oeh.medical.dose.unit'

    # Mantener el string ayuda a que la interfaz no cambie a "Name" o "Desc"
    name = fields.Char(string='Unit', translate=True)
    desc = fields.Char(string='Description', translate=True)

class OeHealthDrugRoute(models.Model):
    _inherit = "oeh.medical.drug.route"

    name = fields.Char(translate=True)
    code = fields.Char(string='Code', translate=True)


class OeHealthDrugForm(models.Model):
    _inherit = "oeh.medical.drug.form"

    name = fields.Char(string='Form', translate=True)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    name = fields.Char(translate=True)

# Heredamos el modelo de producto para que el nombre sea traducible
class ProductProduct(models.Model):
    _inherit = 'product.product'

    name = fields.Char(translate=True)

# 2. Heredamos el modelo médico para las configuraciones
class OeHealthMedicines(models.Model):
    _inherit = 'oeh.medical.medicines'
    
    # Campos que SÍ pertenecen a oeh.medical.medicines
    therapeutic_action = fields.Char(string='Therapeutic effect', translate=True)
    composition = fields.Text(string='Composition', translate=True)
    indications = fields.Text(string='Indication', translate=True)
    dosage = fields.Text(string='Dosage Instructions', translate=True)
    overdosage = fields.Text(string='Overdosage', translate=True)
    pregnancy = fields.Text(string='Pregnancy and Lactancy', translate=True)
    adverse_reaction = fields.Text(string='Adverse Reactions', translate=True)
    storage = fields.Text(string='Storage Conditions', translate=True)
    info = fields.Text(string='Extra Info', translate=True)




