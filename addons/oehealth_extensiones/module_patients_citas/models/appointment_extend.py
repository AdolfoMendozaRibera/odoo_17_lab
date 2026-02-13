from odoo import fields, models, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta

class OeHealthAppointmentExtend(models.Model): 
    
    _inherit = 'oeh.medical.appointment'

    # Solo tus opciones personalizadas
    APPOINTMENT_TYPE = [
        ('Consulta', 'Consulta'),
        ('Re Consulta', 'Re Consulta'),
        ('Colocacion de Suero', 'Colocación de Suero'),
    ]

    # Campo nuevo con nombre personalizado
    appointment_type = fields.Selection(
        APPOINTMENT_TYPE,
        string='Tipo de Cita',
        readonly=False,
        default='Consulta',
        help='Selecciona el tipo de cita'
    )

    name = fields.Char(string='Appointment #', size=64, default='Cita nueva')
    
    # Redefinir para traducción en filtros (no afecta lógica, solo etiqueta)
    appointment_date = fields.Datetime(string='Fecha de Cita', required=True, readonly=False)

    # NUEVOS ESTADOS EXTENDIDOS
    APPOINTMENT_STATUS_EXTENDED = [
        ('Scheduled', 'Programada'),
        ('Completed', 'Realizada'),
        ('Reprogramada', 'Reprogramada'),
        ('Sin Asistir', 'Sin Asistir'),
        ('Invoiced', 'Facturada'),
    ]

   # Agrega esto al inicio de la clase OeHealthAppointmentExtend, después de los campos existentes

    # =================== CAMPO PARA VINCULAR FACTURA ==================
    
    move_id = fields.Many2one(
        'account.move',
        string='Factura',
        readonly=True,
        help='Factura vinculada a esta cita'
    )

    # =================== CAMPO PARA SERVICIO/PRODUCTO CON CÓDIGO ==================
    product_id = fields.Many2one(
        'product.product',
        string='Servicio',
        domain="[('type', '=', 'service')]",
        help='Seleccionar servicio por código o nombre'
    )


    
    # Sobrescribir el campo state completamente
    state = fields.Selection(
        APPOINTMENT_STATUS_EXTENDED,
        string='State',
        readonly=True,
        default='Scheduled',
        track_visibility='onchange'
    )

    color = fields.Integer(string='Color Index', compute='_compute_color_index', store=True)

    # Campo para rastrear la cita original
    parent_appointment_id = fields.Many2one(
        'oeh.medical.appointment',
        string='Cita Original',
        readonly=True,
        help='Referencia a la cita desde la cual se reprogramó esta'
    )

    # =================== CAMPO COMPUTADO PARA ESTADO DE FACTURA ==================
    
    invoice_status = fields.Char(
        string='Estado de la Factura',
        compute='_compute_invoice_status',
        store=True,
        help='Muestra el estado de la factura'
    )
 

    @api.depends('move_id', 'move_id.state', 'state')
    def _compute_invoice_status(self):
        """
        Calcular el estado de la factura según:
        - Si move_id existe y está en borrador → "Por Facturar"
        - Si move_id existe y está confirmado → "Facturado por Completo"
        - Si no hay move_id → "No Facturada"
        """
        for record in self:
            if record.move_id:
                # Si existe factura
                if record.move_id.state == 'draft':
                    record.invoice_status = 'Por Facturar'
                elif record.move_id.state in ('posted', 'paid'):
                    record.invoice_status = 'Facturado por Completo'
                else:
                    record.invoice_status = 'Por Facturar'
            else:
                # Si no existe factura
                record.invoice_status = 'Por Facturar'

    @api.depends('state')
    def _compute_color_index(self):
        for record in self:
            if record.state == 'Scheduled':
                record.color = 4 # Info (Blue)
            elif record.state == 'Completed':
                record.color = 10 # Success (Green)
            elif record.state == 'Reprogramada':
                record.color = 3 # Warning (Yellow)
            elif record.state == 'Sin Asistir':
                record.color = 1 # Danger (Red)
            elif record.state == 'Invoiced':
                record.color = 7 # Muted (Gray/Teal)
            else:
                record.color = 0

    # =================== GENERAR NÚMERO DE CITA AUTOMÁTICAMENTE ==================
    
    @api.model
    def create(self, vals):
        """Generar secuencia antes de crear el registro"""
        # Llamar al método create del padre primero
        record = super(OeHealthAppointmentExtend, self).create(vals)
        
        # Luego verificar y asignar la secuencia si es necesario
        if record.name in ('/', 'Nueva cita', 'Cita nueva', False):
            company = record.company_id or self.env['res.company']._company_default_get('oeh.medical.appointment')
            
            search_sequence = self.env['ir.sequence'].search(
                [('code', '=', 'oeh.medical.appointment'), ('company_id', 'in', [company.id, False])], 
                order='company_id'
            )
            
            if not search_sequence:
                self.env['ir.sequence'].sudo().create({
                    'name': 'Appointments (' + str(company.name) + ')',
                    'code': 'oeh.medical.appointment',
                    'company_id': company.id,
                    'prefix': 'AP',
                    'padding': 4,
                })
            
            # Generar la secuencia y asignarla
            next_number = self.env['ir.sequence'].next_by_code('oeh.medical.appointment')
            record.write({'name': next_number})
        
        return record

    # =================== SOBRESCRIBIR MÉTODOS ORIGINALES DE OEHEALTH ==================
    
    def set_to_invoiced(self):
        """
        Interceptar el botón Facturar para:
        1. Cambiar estado de cita a 'Invoiced' (Facturada)
        2. Crear una cotización (Sale Order)
        3. Llenarla con datos de la cita
        4. Redirigir a la cotización
        """
        self.ensure_one()
        
        # Verificar que la cita esté en estado Completed
        if self.state != 'Completed':
            raise UserError(_('La cita debe estar en estado "Realizada" para ser facturada'))
        
        # PASO 1: CAMBIAR ESTADO A INVOICED INMEDIATAMENTE
        self.write({'state': 'Invoiced'})
        
        # PASO 2: Crear la cotización
        try:
            sale_order = self._create_sale_order_from_appointment()
            
            if not sale_order:
                raise UserError(_('No se pudo crear la cotización'))
            
            # PASO 3: Redirigir a la cotización creada
            return {
                'type': 'ir.actions.act_window',
                'name': _('Cotización Creada'),
                'res_model': 'sale.order',
                'res_id': sale_order.id,
                'view_mode': 'form',
                'target': 'current',
            }
        
        except Exception as e:
            raise UserError(_('Error al crear la cotización: ' + str(e)))


    def _create_sale_order_from_appointment(self):
        """
        Crear una cotización basada en los datos de la cita
        """
        self.ensure_one()
        
        # Obtener datos de la cita
        patient = self.patient
        if not patient:
            raise UserError(_('La cita no tiene paciente asignado'))
        
        partner = patient.partner_id
        if not partner:
            raise UserError(_('El paciente no tiene cliente (partner) vinculado'))
        
        doctor = self.doctor
        if not doctor:
            raise UserError(_('La cita no tiene doctor asignado'))
        
        # Obtener la fecha de la cita
        from datetime import datetime
        appointment_date = self.appointment_date or datetime.now()
        
        if isinstance(appointment_date, str):
            try:
                appointment_date = datetime.strptime(appointment_date, "%Y-%m-%d %H:%M:%S")
            except:
                appointment_date = datetime.now()
        
        # OBTENER LA DIRECCIÓN DE ADMINISTRADOR (por defecto)
        admin_address = self.env['res.partner'].search([
            ('name', '=', 'Administrator'),
        ], limit=1)
        
        if not admin_address:
            admin_address = partner
        
        # Preparar líneas de venta
        sale_order_lines = self._prepare_sale_order_lines()
        
        if not sale_order_lines:
            raise UserError(_('No se pudo preparar las líneas de la cotización'))
        
        # Preparar nota
        appointment_date_str = appointment_date.strftime('%d/%m/%Y %H:%M') if appointment_date else ''
        
        note = f"""INFORMACIÓN DE LA CITA
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Cita #: {self.name}
    Fecha: {appointment_date_str}
    Paciente: {self.patient.name}
    Doctor: {self.doctor.name}
    Tipo de Cita: {self.appointment_type}
    Centro de Salud: {self.institution.name if self.institution else 'N/A'}
    COMENTARIOS:
    {self.comments if self.comments else 'N/A'}"""
        
        # Crear la cotización
        sale_order = self.env['sale.order'].create({
            'partner_id': partner.id,
            'partner_invoice_id': admin_address.id,
            'partner_shipping_id': admin_address.id,
            'date_order': appointment_date,
            'order_line': sale_order_lines,
            'note': note,
            'origin': f'Appointment #{self.name}',
        })
        
        return sale_order

    def _prepare_sale_order_lines(self):
        """
        Preparar las líneas de la cotización - SOLO CONSULTA
        """
        lines = []
        sequence = 1
        
        # 1. LÍNEA DE CONSULTORIA (ENCABEZADO)
        lines.append((0, 0, {
            'name': 'Consulta Médica',
            'display_type': 'line_section',
            'sequence': sequence,
        }))
        sequence += 1
        
        # 2. LÍNEA DE CARGO POR CONSULTA
        consultancy_product = self._get_or_create_consultancy_product()
        
        if not consultancy_product:
            raise UserError(_('No se pudo crear el producto de Consulta'))
        
        # Obtener precio de consulta
        consultancy_price = 0
        if hasattr(self.doctor, 'consultancy_price') and self.doctor.consultancy_price:
            consultancy_price = float(self.doctor.consultancy_price)
        
        lines.append((0, 0, {
            'name': f'Consultancy Charge - Dr. {self.doctor.name}',
            'product_id': consultancy_product.id,
            'product_uom_qty': 1.0,
            'price_unit': consultancy_price,
            'sequence': sequence,
        }))
        
        return lines

    def _prepare_sale_order_note(self):
        """
        Preparar nota de la cotización con información de la cita
        """
        from datetime import datetime
        
        appointment_date = self.appointment_date.strftime('%d/%m/%Y %H:%M') if self.appointment_date else ''
        
        note = f"""
INFORMACIÓN DE LA CITA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Cita #: {self.name}
Fecha: {appointment_date}
Paciente: {self.patient.name}
Doctor: {self.doctor.name}
Tipo de Cita: {self.appointment_type}
Centro de Salud: {self.institution.name if self.institution else ''}

COMENTARIOS:
{self.comments if self.comments else 'N/A'}
"""
        return note

    def _get_or_create_consultancy_product(self):
        """
        Obtener o crear un producto para "Consulta Médica"
        """
        # Primero buscar por código
        product = self.env['product.product'].search(
            [('default_code', '=', 'CONSULT-001')],
            limit=1
        )
        
        # Si no existe por código, buscar por nombre
        if not product:
            product = self.env['product.product'].search(
                [('name', '=', 'Consulta Médica'), ('type', '=', 'service')],
                limit=1
            )
        
        # Si aún no existe, crear uno nuevo
        if not product:
            try:
                # Usar product.template.create que es más seguro
                template = self.env['product.template'].create({
                    'name': 'Consulta Médica',
                    'type': 'service',
                    'list_price': 0.0,
                    'sale_ok': True,
                    'default_code': 'CONSULT-001',
                })
                
                # Obtener la variante de producto
                if template.product_variant_ids:
                    product = template.product_variant_ids[0]
            except Exception as e:
                raise UserError(_('Error al crear producto de consulta: ') + str(e))
        
        return product

    def _get_or_create_medicine_product(self, medicine):
        """
        Obtener o crear un producto para una medicina
        """
        try:
            if not medicine or not hasattr(medicine, 'name'):
                return False
            
            # VALIDACIÓN: Verificar que el nombre sea válido
            medicine_name = medicine.name
            if not medicine_name or (isinstance(medicine_name, str) and medicine_name.strip() == ''):
                return False
            
            product = self.env['product.product'].search(
                [('name', '=', str(medicine_name))],
                limit=1
            )
            
            if not product:
                product = self.env['product.product'].create({
                    'name': str(medicine_name),
                    'type': 'product',
                    'list_price': 0,
                    'sale_ok': True,
                })
            
            return product
        
        except Exception as e:
            return False
    
    # =================== MÉTODOS PERSONALIZADOS ==================
    
    def action_mark_sin_asistir(self):
        """Cambiar estado a Sin Asistir"""
        for record in self:
            if record.state == 'Scheduled':
                record.write({'state': 'Sin Asistir'})
            else:
                raise UserError(_('Solo puedes marcar como Sin Asistir si la cita está Programada'))
        return True
    
    def action_reprogramar(self):
        """Abrir wizard para reprogramar cita"""
        self.ensure_one()
        
        if self.state == 'Invoiced':
            raise UserError(_('No puedes reprogramar una cita que ya fue facturada'))
        
        return {
            'name': _('Reprogramar Cita'),
            'type': 'ir.actions.act_window',
            'res_model': 'appointment.reprogramar.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_appointment_id': self.id},
        }
    
    def create_duplicate_appointment(self, new_date, notes=False):
        """Crear duplicado de cita con nueva fecha"""
        self.ensure_one()
        
        from datetime import datetime
        # Convert new_date to datetime if it is a string (defensive programming)
        if isinstance(new_date, str):
            new_date = datetime.strptime(new_date, "%Y-%m-%d %H:%M:%S")

        if new_date <= datetime.now():
            raise UserError(_('La nueva fecha debe ser en el futuro'))
        
        # 1. Actualizar cita original
        old_comments = self.comments or ''
        # Avoid double updating if already reprogrammed recently or just append cleanly
        reprogram_note = f"\n[Reprogramada el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]"
        if notes:
            reprogram_note += f"\nNuevas notas: {notes}"
            
        self.write({
            'state': 'Reprogramada',
            'comments': old_comments + reprogram_note
        })
        
        # 2. Preparar comentarios para nueva cita
        new_comments = f"Cita reprogramada desde {self.name}"
        if notes:
            new_comments += f"\n{notes}"

        # 3. Crear nueva cita
        return self.create({
            # Let name be generated by sequence
            'patient': self.patient.id,
            'doctor': self.doctor.id,
            'appointment_date': new_date,
            'duration': self.duration,
            'institution': self.institution.id,
            'appointment_type': self.appointment_type,
            'urgency_level': self.urgency_level,
            'patient_status': self.patient_status,
            'comments': new_comments,
            'state': 'Scheduled',
            'parent_appointment_id': self.id,
        })
    
    # =================== PERMITIR BORRAR SIN RESTRICCIONES ==================
    
    def unlink(self):
        """
        Permite borrar citas en cualquier estado.
        Sobrescribe el método de la clase base que tiene restricciones.
        """
        return super(models.Model, self).unlink()


    
     # ======================== CAMPO PARA HORA DE FINAL ========================
    # NUEVO NOMBRE para evitar conflicto con el Float anterior
    
    appointment_final_datetime = fields.Datetime(
        string='Hora de Final',
        help='Fecha y hora de fin de la cita (por defecto +20 min desde fecha de inicio)',
        required=False
    )

    # ======================== MÉTODOS AUXILIARES ========================

    @api.onchange('appointment_date')
    def _onchange_appointment_date(self):
        """Cuando cambia la fecha, suma 20 minutos para hora final"""
        if self.appointment_date:
            self.appointment_final_datetime = self.appointment_date + timedelta(minutes=20)

    @api.constrains('appointment_date', 'appointment_final_datetime')
    def _check_appointment_times(self):
        """Valida que la hora de fin sea mayor a la fecha de inicio"""
        for record in self:
            if record.appointment_date and record.appointment_final_datetime:
                if record.appointment_date >= record.appointment_final_datetime:
                    raise UserError(_('La hora de fin debe ser mayor a la fecha de inicio'))