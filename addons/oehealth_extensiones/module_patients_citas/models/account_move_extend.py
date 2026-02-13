from odoo import models, api, fields

class AccountMoveExtend(models.Model):
    _inherit = 'account.move'
    
    @api.model
    def create(self, vals):
        """
        Vincular automáticamente la factura a la cita cuando se crea
        """
        move = super(AccountMoveExtend, self).create(vals)
        
        try:
            # MÉTODO 1: Buscar por líneas de la factura → orden de venta → cita
            if move.line_ids:
                for line in move.line_ids:
                    # Cada línea tiene referencia a sale_line_ids
                    if hasattr(line, 'sale_line_ids') and line.sale_line_ids:
                        for sale_line in line.sale_line_ids:
                            sale_order = sale_line.order_id
                            
                            if sale_order and sale_order.origin:
                                origin_clean = sale_order.origin.replace('Appointment #', '').strip()
                                
                                appointment = self.env['oeh.medical.appointment'].search(
                                    [('name', '=', origin_clean)],
                                    limit=1
                                )
                                
                                if appointment:
                                    # Vincular la factura a la cita
                                    appointment.write({'move_id': move.id})
                                    return move
            
            # MÉTODO 2: Si MÉTODO 1 falla, buscar por invoice_origin
            invoice_origin = move.ref or move.invoice_origin
            
            if invoice_origin:
                origin_clean = invoice_origin.replace('Appointment #', '').strip()
                
                appointment = self.env['oeh.medical.appointment'].search(
                    [('name', '=', origin_clean)],
                    limit=1
                )
                
                if appointment:
                    appointment.write({'move_id': move.id})
        
        except Exception as e:
            # Si hay error, simplemente continuar sin vincular
            pass
        
        return move
    
    def write(self, vals):
        """
        Actualizar el estado de la factura en la cita cuando cambia
        """
        res = super(AccountMoveExtend, self).write(vals)
        
        # Si cambió el estado, actualizar la cita
        if 'state' in vals:
            for move in self:
                try:
                    # MÉTODO 1: Buscar por líneas
                    if move.line_ids:
                        for line in move.line_ids:
                            if hasattr(line, 'sale_line_ids') and line.sale_line_ids:
                                for sale_line in line.sale_line_ids:
                                    sale_order = sale_line.order_id
                                    
                                    if sale_order and sale_order.origin:
                                        origin_clean = sale_order.origin.replace('Appointment #', '').strip()
                                        
                                        appointment = self.env['oeh.medical.appointment'].search(
                                            [('name', '=', origin_clean)],
                                            limit=1
                                        )
                                        
                                        if appointment:
                                            appointment.move_id = move.id
                                            break
                    
                    # MÉTODO 2: Si falla, buscar por invoice_origin
                    if not move.line_ids or not any(hasattr(l, 'sale_line_ids') for l in move.line_ids):
                        invoice_origin = move.ref or move.invoice_origin
                        
                        if invoice_origin:
                            origin_clean = invoice_origin.replace('Appointment #', '').strip()
                            
                            appointment = self.env['oeh.medical.appointment'].search(
                                [('name', '=', origin_clean)],
                                limit=1
                            )
                            
                            if appointment:
                                appointment.move_id = move.id
                
                except Exception as e:
                    pass
        
        return res