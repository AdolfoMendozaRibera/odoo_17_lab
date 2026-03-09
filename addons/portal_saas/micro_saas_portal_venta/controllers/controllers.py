# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSaleSaas(WebsiteSale):
    
    @http.route(['/shop/cart/update'], type='http', auth="public", methods=['POST'], website=True)
    def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
        """
        Sobrescribe controlador de carrito de compras para atrapar 
        `x_months` y `x_users` mandados por el formulario.
        """
        # Obtenemos los valores enviados desde el frontend, con defaults en 1
        x_months = kw.get('x_months', 0)
        x_users = kw.get('x_users', 0)
        
        # Ejecutamos el controlador base de Odoo para añadir el producto al carrito
        res = super(WebsiteSaleSaas, self).cart_update(product_id=product_id, add_qty=add_qty, set_qty=set_qty, **kw)
        
        # Una vez creada o actualizada la línea del carrito, buscamos la orden activa
        order = request.website.sale_get_order()
        if order and order.state != 'cancel':
            # Localizamos la línea que corresponde al producto de suscripción
            line = order.order_line.filtered(lambda l: l.product_id.id == int(product_id))
            if line and line.product_id.is_subscription:
                # Escribimos los valores de meses y usuarios capturados del formulario
                # y forzamos el recálculo del precio unitario basado en nuestra fórmula
                vals = {
                    'x_months': int(x_months) if x_months else 1,
                    'x_users': int(x_users) if x_users else 1,
                }
                line.sudo().write(vals)
                
                # Buscamos romper la sincronización automática con la lista de precios 
                # para este producto específico (SaaS). Usamos el list price base.
                precio_base = line.product_id.lst_price
                nuevo_precio = line.x_months * line.x_users * precio_base
                
                # Hacemos un write forzoso sobre price_unit para retener nuestro valor dinámico
                line.sudo().write({'price_unit': nuevo_precio})
                
                # Aseguramos que el total de la orden se recalcule de inmediato
                order._amount_all()
                    
        return res

    @http.route(['/my/subscription/renew/<int:subscription_id>'], type='http', auth='user', website=True)
    def renew_subscription(self, subscription_id, **kw):
        """
        Punto extra (Opcional): Ruta en el portal para "Renovar Suscripción" ("Flujo de Renovación").
        """
        # Asegurarse que el usuario logueado es el dueño
        sub = request.env['subscription.package'].sudo().browse(subscription_id)
        if not sub.exists() or sub.partner_id.id != request.env.user.partner_id.id:
            return request.redirect('/my')

        # Aquí podríamos renderizar un wizard o un formulario similar al del producto
        # para que escoja nuevos meses y usuarios
        return request.render('micro_saas_portal_venta.portal_renewal_form', {'subscription': sub})
