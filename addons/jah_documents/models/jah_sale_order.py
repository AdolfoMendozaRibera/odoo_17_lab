# -*- coding: utf-8 -*-

from odoo import models, fields, api


class JahSaleOrder(models.Model):
    """
    Extensión del modelo sale.order para incluir campos adicionales
    relacionados con la personalización de documentos JAH
    """
    _inherit = 'sale.order'

class JahSaleOrderLine(models.Model):
    """
    Extensión del modelo sale.order.line para asegurar que todos los campos
    necesarios estén disponibles en los reportes
    """
    _inherit = 'sale.order.line'