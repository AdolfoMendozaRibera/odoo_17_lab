from odoo import api, fields, models, _
from odoo.exceptions import UserError

class OeHealthDoctor(models.Model):
    _inherit = 'oeh.medical.physician'

    # Campo computado para el contador de citas atendidas
    appointment_count = fields.Integer(
        string='Pacientes Atendidos',
        compute='_compute_appointment_count',
        store=False  # No guardamos en BD para que se recalcule al filtrar
    )

    def _compute_appointment_count(self):
        Appointment = self.env['oeh.medical.appointment']
        for doc in self:
            # Contar citas completadas
            # Se pueden añadir filtros adicionales por fecha si se requieren en el contexto
            domain = [
                ('doctor', '=', doc.id),
                ('state', '=', 'Completed') 
            ]
            doc.appointment_count = Appointment.search_count(domain)

    def action_view_appointments_report(self):
        self.ensure_one()
        return {
            'name': 'Pacientes Atendidos',
            'type': 'ir.actions.act_window',
            'res_model': 'oeh.medical.appointment',
            'view_mode': 'tree,form,graph',
            'domain': [('doctor', '=', self.id), ('state', '=', 'Completed')],
            'context': {'search_default_group_date': 1} # Agrupación por defecto si se desea
        }

# 1. MODELO DE ESTACIONES (Nuevo)
class OeHealthStation(models.Model):
    _name = 'oeh.medical.station'
    _description = 'Estación de Atención'

    name = fields.Char(string='Nombre de Estación', required=True)
    # Vinculamos la estación a una ubicación de inventario (Ej: Bodega Enfermería 1)
    stock_location_id = fields.Many2one(
        'stock.location', 
        string='Ubicación de Stock', 
        required=True,
        domain=[('usage', '=', 'internal')],
        help="Ubicación desde donde se descontarán los insumos usados en esta estación."
    )

# 2. MODELO PARA LÍNEAS DE CONSUMO (Nuevo)
class OeHealthAppointmentConsumable(models.Model):
    _name = 'oeh.medical.appointment.consumable'
    _description = 'Línea de Consumo de Insumos'

    appointment_id = fields.Many2one('oeh.medical.appointment', string='Cita')
    product_id = fields.Many2one('product.product', string='Insumo/Medicamento', required=True)
    qty = fields.Float(string='Cantidad Usada', default=1.0, required=True)
    notes = fields.Char(string='Notas/Observaciones')

# 3. HERENCIA DE CITAS (Modificación)
class OeHealthAppointmentInherit(models.Model):
    _inherit = 'oeh.medical.appointment'

    # Campos nuevos
    station_id = fields.Many2one('oeh.medical.station', string='Estación de Atención')
    
    # Campo One2many para los insumos
    consumable_line_ids = fields.One2many(
        'oeh.medical.appointment.consumable', 
        'appointment_id', 
        string='Consumo de Insumos'
    )

    # Extender estado 'state' si el original es Selection. 
    # NOTA: Si el campo original es selection estático, a veces es mejor redeclararlo o usar un campo nuevo.
    # Asumiremos que nos enganchamos al flujo existente agregando un paso.
    state = fields.Selection(selection_add=[('in_process', 'En Proceso')], ondelete={'in_process': 'cascade'})

    def action_start_process(self):
        """ Cambia estado a En Proceso, validando la Estación """
        for rec in self:
            if not rec.station_id:
                raise UserError(_("Debe seleccionar una 'Estación de Atención' antes de iniciar."))
            rec.write({'state': 'in_process'})

    def action_appointment_done(self): # Asegúrate que este sea el nombre del método original del botón 'Done'
        """ Al finalizar, descuenta inventario """
        res = super(OeHealthAppointmentInherit, self).action_appointment_done() # Llamar lógica original
        
        for rec in self:
            if rec.consumable_line_ids and rec.station_id.stock_location_id:
                rec._create_stock_move_for_consumables()
        
        return res

    def _create_stock_move_for_consumables(self):
        """ Genera el Picking de salida """
        stock_picking_obj = self.env['stock.picking']
        move_obj = self.env['stock.move']
        
        # Buscar tipo de operación de salida por defecto del almacén de la ubicación
        warehouse = self.env['stock.location'].browse(self.station_id.stock_location_id.id).get_warehouse()
        picking_type = self.env['stock.picking.type'].search([
            ('code', '=', 'outgoing'),
            ('warehouse_id', '=', warehouse.id)
        ], limit=1)

        if not picking_type:
             raise UserError(_("No se encontró un tipo de operación de salida para la ubicación seleccionada."))

        # Crear cabecera del Picking
        picking = stock_picking_obj.create({
            'partner_id': self.patient.partner_id.id, # Asumiendo que 'patient' tiene relación con 'res.partner'
            'picking_type_id': picking_type.id,
            'location_id': self.station_id.stock_location_id.id,
            'location_dest_id': self.env.ref('stock.stock_location_customers').id, # Salida a Clientes
            'origin': self.name,
        })

        # Crear movimientos
        for line in self.consumable_line_ids:
            move_obj.create({
                'name': f"Consumo cita {self.name}",
                'product_id': line.product_id.id,
                'product_uom_qty': line.qty,
                'product_uom': line.product_id.uom_id.id,
                'picking_id': picking.id,
                'location_id': self.station_id.stock_location_id.id,
                'location_dest_id': self.env.ref('stock.stock_location_customers').id,
            })

        # Confirmar y validar picking automáticamente si se desea
        picking.action_confirm()
        picking.action_assign()
        picking.button_validate()
