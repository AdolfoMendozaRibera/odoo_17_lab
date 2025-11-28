# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    """
    Extensión del modelo sale.order para incluir campos adicionales
    relacionados con la personalización de documentos JAH
    """
    _inherit = 'sale.order'

    require_signature = fields.Boolean(
        string='Requiere Firma',
        default=True,
        help="Si está marcado, se mostrará un espacio para firma del cliente en la orden de venta."
    )


class SaleOrderLine(models.Model):
    """
    Extensión del modelo sale.order.line para asegurar que todos los campos
    necesarios estén disponibles en los reportes
    """
    _inherit = 'sale.order.line'