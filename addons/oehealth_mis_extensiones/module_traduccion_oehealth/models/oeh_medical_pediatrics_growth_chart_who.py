from odoo import fields, models

class OeHealthPediatricsGrowthChart(models.Model):
    _inherit = "oeh.medical.pediatrics.growth.chart.who"

    # Si el campo 'type' muestra info descriptiva
    type = fields.Char(string='Type', size=56, translate=True)