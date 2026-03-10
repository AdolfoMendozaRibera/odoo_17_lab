# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSaleSaas(WebsiteSale):
    
    @http.route(['/shop/cart/update'], type='http', auth="public", methods=['POST'], website=True)
    def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
        """
        Sobrescribe controlador de carrito de compras para atrapar 
        `x_months` y `x_users` mandados por el formulario dinámico del frontend.
        Lógica Vital: Esta es la puerta de entrada de los valores que el usuario elige en el portal.
        """
        # Obtenemos los valores enviados desde el frontend (posiblemente inyectados por JS)
        x_months = kw.get('x_months', 0)
        x_users = kw.get('x_users', 0)
        
        # Ejecutamos el flujo estándar de Odoo para añadir el producto al carrito
        res = super(WebsiteSaleSaas, self).cart_update(product_id=product_id, add_qty=add_qty, set_qty=set_qty, **kw)
        
        # Una vez creada o actualizada la línea del carrito, buscamos la orden activa
        order = request.website.sale_get_order()
        if order and order.state != 'cancel':
            # Localizamos la línea que corresponde al producto de suscripción recién añadido/actualizado
            line = order.order_line.filtered(lambda l: l.product_id.id == int(product_id))
            if line and line.product_id.is_subscription:
                # Escribimos los valores de meses y usuarios capturados del formulario
                # Nota: Se asume que estos campos existen en la línea (heredados de subscription_package_mejora)
                vals = {
                    'x_months': int(x_months) if x_months else 1,
                    'x_users': int(x_users) if x_users else 1,
                }
                line.sudo().write(vals)
                
                # RECALCULO DINÁMICO DE PRECIO:
                # Rompe la sincronización con la lista de precios estándar de Odoo.
                # El precio se calcula como: Meses x Usuarios x Precio Base del Producto.
                precio_base = line.product_id.lst_price
                nuevo_precio = line.x_months * line.x_users * precio_base
                
                # Forzamos el valor en price_unit para que no sea sobrescrito por un pricelist
                line.sudo().write({'price_unit': nuevo_precio})
                
                # Recalculamos los totales del pedido
                order._amount_all()
                    
        return res

    @http.route(['/my/subscription/renew/<int:subscription_id>'], type='http', auth='user', website=True)
    def renew_subscription(self, subscription_id, **kw):
        """
        Ruta en el portal para "Renovar Suscripción".
        Permite al usuario volver al flujo de compra para extender su suscripción actual.
        """
        # Verificación de seguridad: Dueño de la suscripción
        sub = request.env['subscription.package'].sudo().browse(subscription_id)
        if not sub.exists() or sub.partner_id.id != request.env.user.partner_id.id:
            return request.redirect('/my')

        # Renderiza un formulario específico para la renovación (configuración de nuevos meses/usuarios)
        return request.render('micro_saas_portal_venta.portal_renewal_form', {'subscription': sub})
