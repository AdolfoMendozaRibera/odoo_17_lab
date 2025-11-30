from odoo import fields, models, api
from odoo.exceptions import ValidationError

class ResCompany(models.Model):
    _inherit = 'res.company'

    company_nit = fields.Char(
        string='NIT de la Compañía', 
        help="Número de Identificación Tributaria (NIT) usado para reportes JAH."
    )
    
    company_casa_matriz_address = fields.Char(
        string='Dirección Casa Matriz', 
        help="Dirección específica a mostrar en el encabezado de los reportes."
    )
    
    @api.constrains('company_nit')
    def _check_nit_format(self):
        """Validación básica del NIT (opcional según Bolivia)"""
        for record in self:
            if record.company_nit and not record.company_nit.replace('-', '').isdigit():
                raise ValidationError("El NIT debe contener solo números y guiones")