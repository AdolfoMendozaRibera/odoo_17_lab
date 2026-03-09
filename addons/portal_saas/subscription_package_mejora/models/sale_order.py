from odoo import models, fields, api
import math

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Tipo de orden para distinguir lógicas de renovación o ampliación
    x_order_type = fields.Selection([
        ('new', 'Nueva Suscripción'),
        ('addon', 'Adición de Usuarios'),
        ('renewal', 'Renovación')
    ], string='Tipo de Orden', default='new', tracking=True)
    
    # Enlace a la suscripción existente cuando es addon o renewal
    x_parent_subscription_id = fields.Many2one(
        'subscription.package', string='Suscripción Padre', 
        help="Suscripción a la cual se le aplicará la renovación o adición de usuarios."
    )

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    x_months = fields.Integer(string='Meses Contratados', default=0)
    x_users = fields.Integer(string='Cantidad de Usuarios', default=0)

    @api.onchange('product_id', 'x_months', 'x_users', 'order_id.x_parent_subscription_id')
    def _onchange_saas_metrics(self):
        """
        Calculo dinámico para la interfaz del backend.
        """
        self._compute_saas_price_unit()

    def _compute_saas_price_unit(self):
        """
        Calcula el precio dinámico de la suscripción basado en meses y usuarios.
        Aplica la fórmula: Usuarios * Meses * 50 Bs.
        """
        for line in self:
            if line.product_id and line.product_id.is_subscription:
                # Usamos el precio del producto (lista de precios/catalogo) en lugar de hardcodear 50
                precio_base = line.product_id.lst_price
                
                # Lógica de co-terminación para Addons
                if line.order_id.x_order_type == 'addon' and line.order_id.x_parent_subscription_id:
                    sub = line.order_id.x_parent_subscription_id
                    if sub.date_started and sub.close_date:
                        today = fields.Date.context_today(self)
                        if today > sub.close_date:
                            meses_restantes = 0
                        else:
                            diferencia_dias = (sub.close_date - today).days
                            meses_restantes = math.ceil(diferencia_dias / 30.0)
                        
                        line.x_months = meses_restantes
                        line.price_unit = line.x_users * meses_restantes * precio_base
                else:
                    # Caso Base / Renovación
                    if line.x_months > 0 and line.x_users > 0:
                        line.price_unit = line.x_users * line.x_months * precio_base

    def _get_display_price(self):
        """
        Sobrescribimos este método (usado por website_sale) para asegurar que 
        el precio mostrado en el carrito y checkout sea el calculado por nuestra lógica SaaS
        en lugar del precio base del producto/lista de precios.
        Rompe la sincronización automática con la lista de precios para este producto específico.
        """
        price = super()._get_display_price()
        if self.product_id.is_subscription and self.x_months > 0 and self.x_users > 0:
            # Multiplicamos por el precio real del producto (lst_price) para ser dinámicos
            return self.x_users * self.x_months * self.product_id.lst_price
        return price

    @api.depends('product_id', 'product_uom', 'product_uom_qty')
    def _compute_price_unit(self):
        """
        Sobrescribimos la computación estandar de odoo 17. 
        Si recarga en checkout, forzará a usar nuestra suscripción para que el invoice 
        se lleve el precio unitario saas de N usuarios x M meses y evite la pricelist.
        """
        super()._compute_price_unit()
        for line in self:
            if line.product_id and line.product_id.is_subscription:
                if line.x_months > 0 and line.x_users > 0:
                    precio_base = line.product_id.lst_price
                    line.price_unit = line.x_users * line.x_months * precio_base
