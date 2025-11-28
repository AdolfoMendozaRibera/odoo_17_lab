# -*- coding: utf-8 -*-

from odoo import fields, models


class ResCompany(models.Model):
    """
    Extiende el modelo res.company para agregar campos de identificación fiscal
    y configuración necesarios para el encabezado de los reportes JAH.
    """
    _inherit = 'res.company'

    company_nit = fields.Char(
        string='NIT de la Compañía', 
        help="Número de Identificación Tributaria (NIT) usado para reportes JAH."
    )
    
    company_casa_matriz_address = fields.Char(
        string='Dirección Casa Matriz', 
        help="Dirección específica a mostrar en el encabezado de los reportes."
    )