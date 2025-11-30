# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPicking(models.Model):
    """
    Extensión del modelo stock.picking para incluir campos adicionales
    relacionados con la personalización de documentos JAH
    """
    _inherit = 'stock.picking'

    delivery_responsible = fields.Char(
        string='Responsable de Entrega',
        help="Nombre del responsable que entrega el material"
    )
    
    receiver_name = fields.Char(
        string='Nombre de quien Recibe',
        help="Nombre de la persona que recibe el material"
    )
    
    receiver_id_number = fields.Char(
        string='CI del Receptor',
        help="Número de Cédula de Identidad de quien recibe"
    )


class StockMove(models.Model):
    """
    Extensión del modelo stock.move para asegurar que todos los campos
    necesarios estén disponibles en los reportes
    """
    _inherit = 'stock.move'
    
    # Odoo ya tiene los campos necesarios:
    # - product_id.default_code (código)
    # - name (descripción)
    # - product_uom (unidad)
    # - product_uom_qty (cantidad ordenada)
    # - quantity (cantidad entregada)