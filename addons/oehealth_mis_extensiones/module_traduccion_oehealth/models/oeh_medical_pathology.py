from odoo import fields, models

class OeHealthPathologyCategory(models.Model):
    _inherit = 'oeh.medical.pathology.category'
    name = fields.Char(string='Category Name', translate=True)

class OeHealthPathology(models.Model):
    _inherit = 'oeh.medical.pathology'
    name = fields.Char(string='Disease Name', translate=True)
    info = fields.Text(string='Extra Info', translate=True) # Te sugiero agregar este también