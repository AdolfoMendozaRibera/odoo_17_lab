from odoo import fields, models

class OeHealthWhatsappTemplate(models.Model):
    _inherit = 'oeh.medical.whatsapp.template'

    # Al agregar translate=True, habilitas el ícono de globo 
    # y permites que Odoo busque estos textos en el archivo .po
    name = fields.Char(string="Title", translate=True)
    message = fields.Text(string="Message", translate=True)