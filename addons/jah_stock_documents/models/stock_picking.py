# -*- coding: utf-8 -*-

from odoo import models

class StockPicking(models.Model):
    """
    Extensión del modelo stock.picking para JAH
    """
    _inherit = 'stock.picking'
    
    # No se necesitan campos adicionales