# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date

class Tarea(models.Model):
    """
    Modelo principal: Tareas.
    Incluye todos los tipos de relaciones y ejemplos de APIs.
    """
    
    _name = 'mi_gestor_tareas.tarea'
    _description = 'Tarea'
    _order = 'fecha_limite desc, prioridad desc'
    
    # Herencia de mail.thread para agregar chatter (mensajes y seguidores)
    # Esta es herencia por EXTENSIÓN (_inherit sin _name)
    # pero en este caso creamos un modelo nuevo que usa funcionalidades de mail
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    # ====================
    # CAMPOS BÁSICOS
    # ====================
    
    nombre = fields.Char(
        string='Nombre de la Tarea',
        required=True,
        tracking=True,  # Registra cambios en el chatter
        help='Título descriptivo de la tarea'
    )
    
    descripcion = fields.Html(
        string='Descripción',
        help='Descripción detallada de la tarea'
    )
    
    # Selection con estado de la tarea
    estado = fields.Selection([
        ('nuevo', 'Nuevo'),
        ('en_progreso', 'En Progreso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ], string='Estado', default='nuevo', required=True, tracking=True)
    
    # Selection con prioridad
    prioridad = fields.Selection([
        ('0', 'Baja'),
        ('1', 'Media'),
        ('2', 'Alta'),
        ('3', 'Urgente'),
    ], string='Prioridad', default='1')
    
    # ====================
    # CAMPOS DE FECHA
    # ====================
    
    fecha_creacion = fields.Date(
        string='Fecha de Creación',
        default=fields.Date.today,  # Función que devuelve la fecha de hoy
        readonly=True
    )
    
    fecha_limite = fields.Date(
        string='Fecha Límite',
        tracking=True
    )
    
    # Datetime: fecha y hora
    fecha_completado = fields.Datetime(
        string='Fecha de Completado',
        readonly=True
    )
    
    # ====================
    # CAMPOS NUMÉRICOS
    # ====================
    
    progreso = fields.Float(
        string='Progreso (%)',
        default=0.0,
        help='Porcentaje de avance de la tarea'
    )
    
    horas_estimadas = fields.Float(
        string='Horas Estimadas',
        default=1.0
    )
    
    horas_reales = fields.Float(
        string='Horas Reales',
        default=0.0
    )
    
    # ====================
    # RELACIONES
    # ====================
    
    # Many2one: relación muchos a uno
    # Muchas tareas pueden tener la misma categoría
    categoria_id = fields.Many2one(
        comodel_name='mi_gestor_tareas.categoria',
        string='Categoría',
        ondelete='restrict',  # No permitir eliminar categoría si tiene tareas
        tracking=True
    )
    
    # Many2one con modelo del módulo base
    # res.partner es el modelo de contactos/clientes de Odoo
    responsable_id = fields.Many2one(
        comodel_name='res.partner',
        string='Responsable',
        tracking=True
    )
    
    # Many2many: relación muchos a muchos con etiquetas
    etiqueta_ids = fields.Many2many(
        comodel_name='mi_gestor_tareas.etiqueta',
        string='Etiquetas'
    )
    
    # ====================
    # CAMPOS COMPUTADOS
    # ====================
    
    # Compute: campo calculado automáticamente
    dias_restantes = fields.Integer(
        string='Días Restantes',
        compute='_compute_dias_restantes',
        store=False  # No guardarlo en BD, calcularlo siempre
    )
    
    # Campo related: "atajo" para acceder a un campo de un registro relacionado
    # Es como hacer: self.categoria_id.color
    color_categoria = fields.Selection(
        related='categoria_id.color',
        string='Color de Categoría',
        readonly=True
    )
    
    vencida = fields.Boolean(
        string='Vencida',
        compute='_compute_vencida',
        search='_search_vencida'  # Permite buscar por este campo
    )
    
    # ====================
    # MÉTODOS COMPUTE
    # ====================
    
    @api.depends('fecha_limite')
    def _compute_dias_restantes(self):
        """Calcula los días que faltan para la fecha límite."""
        hoy = date.today()
        for record in self:
            if record.fecha_limite:
                delta = record.fecha_limite - hoy
                record.dias_restantes = delta.days
            else:
                record.dias_restantes = 0
    
    @api.depends('fecha_limite', 'estado')
    def _compute_vencida(self):
        """Determina si la tarea está vencida."""
        hoy = date.today()
        for record in self:
            if record.fecha_limite and record.estado not in ['completado', 'cancelado']:
                record.vencida = record.fecha_limite < hoy
            else:
                record.vencida = False
    
    # Método search personalizado para campo computado
    def _search_vencida(self, operator, value):
        """
        Permite buscar tareas vencidas.
        Se usa cuando haces: self.search([('vencida', '=', True)])
        """
        hoy = fields.Date.today()
        if operator == '=' and value:
            return [
                ('fecha_limite', '<', hoy),
                ('estado', 'not in', ['completado', 'cancelado'])
            ]
        else:
            return [
                '|',
                ('fecha_limite', '>=', hoy),
                ('estado', 'in', ['completado', 'cancelado'])
            ]
    
    # ====================
    # MÉTODOS ONCHANGE
    # ====================
    
    # @api.onchange: se ejecuta solo en la UI cuando cambia el campo
    # NO modifica la base de datos hasta que guardes
    @api.onchange('progreso')
    def _onchange_progreso(self):
        """
        Si el progreso llega a 100%, cambia el estado automáticamente.
        Esto solo pasa en el formulario, no en la BD hasta guardar.
        """
        if self.progreso >= 100:
            self.estado = 'completado'
            # Retornar un warning (mensaje emergente en la UI)
            return {
                'warning': {
                    'title': _('Tarea Completada'),
                    'message': _('La tarea se ha marcado como completada automáticamente.')
                }
            }
    
    @api.onchange('estado')
    def _onchange_estado(self):
        """Actualiza el progreso según el estado."""
        if self.estado == 'completado':
            self.progreso = 100.0
        elif self.estado == 'nuevo':
            self.progreso = 0.0
    
    # ====================
    # RESTRICCIONES
    # ====================
    
    _sql_constraints = [
        ('progreso_valido', 'CHECK(progreso >= 0 AND progreso <= 100)',
         'El progreso debe estar entre 0 y 100'),
        ('horas_positivas', 'CHECK(horas_estimadas >= 0 AND horas_reales >= 0)',
         'Las horas deben ser positivas'),
    ]
    
    @api.constrains('fecha_limite', 'fecha_creacion')
    def _check_fechas(self):
        """Valida que la fecha límite no sea anterior a la creación."""
        for record in self:
            if record.fecha_limite and record.fecha_creacion:
                if record.fecha_limite < record.fecha_creacion:
                    raise ValidationError(
                        'La fecha límite no puede ser anterior a la fecha de creación'
                    )
    
    # ====================
    # MÉTODOS DE ACCIÓN
    # ====================
    
    def action_marcar_completada(self):
        """
        Método llamado desde un botón en la vista.
        Marca la tarea como completada.
        """
        # self puede ser un recordset con varios registros
        # Este método funciona con uno o varios a la vez
        for record in self:
            record.write({
                'estado': 'completado',
                'progreso': 100.0,
                'fecha_completado': fields.Datetime.now()
            })
        
        # Retornar notificación tipo toast
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Éxito'),
                'message': _('Tarea(s) marcada(s) como completada(s)'),
                'type': 'success',
                'sticky': False,
            }
        }
    
    def action_marcar_en_progreso(self):
        """Cambia el estado a 'en progreso'."""
        self.write({'estado': 'en_progreso'})
    
    def action_cancelar(self):
        """Cancela la tarea."""
        self.write({'estado': 'cancelado'})
    
    # ====================
    # HERENCIA DE MÉTODOS
    # ====================
    
    @api.model
    def create(self, vals):
        """
        Sobrescribe create para agregar lógica personalizada.
        Se ejecuta al crear una nueva tarea.
        """
        # Validar que tenga responsable si la prioridad es alta
        if vals.get('prioridad') == '3' and not vals.get('responsable_id'):
            raise UserError('Las tareas urgentes deben tener un responsable asignado')
        
        # Crear el registro
        tarea = super(Tarea, self).create(vals)
        
        # Enviar mensaje al chatter (gracias a mail.thread)
        tarea.message_post(
            body=f"Tarea '{tarea.nombre}' creada correctamente.",
            message_type='notification'
        )
        
        return tarea
    
    def write(self, vals):
        """
        Sobrescribe write para lógica al modificar.
        """
        # Si se marca como completada, guardar fecha
        if vals.get('estado') == 'completado':
            vals['fecha_completado'] = fields.Datetime.now()
            vals['progreso'] = 100.0
        
        # Ejecutar el write original
        result = super(Tarea, self).write(vals)
        
        # Enviar notificación si cambió el estado
        if 'estado' in vals:
            for record in self:
                record.message_post(
                    body=f"Estado cambiado a: {dict(record._fields['estado'].selection).get(record.estado)}",
                    message_type='notification'
                )
        
        return result
    
    @api.ondelete(at_uninstall=False)
    def _check_delete(self):
        """
        Valida antes de eliminar.
        NO sobrescribir unlink, usar @api.ondelete.
        """
        for record in self:
            if record.estado == 'en_progreso':
                raise UserError(
                    f'No se puede eliminar la tarea "{record.nombre}" '
                    f'porque está en progreso. Cancélala primero.'
                )
    
    # ====================
    # MÉTODO PROGRAMADO (CRON)
    # ====================
    
    @api.model
    def limpiar_vencidas(self):
        """
        Método que será llamado por un cron automático.
        Cancela tareas vencidas hace más de 30 días.
        """
        fecha_limite = fields.Date.today()
        # Buscar tareas vencidas hace más de 30 días
        tareas = self.search([
            ('fecha_limite', '<', fecha_limite),
            ('estado', '=', 'nuevo'),
        ])
        
        if tareas:
            tareas.write({'estado': 'cancelado'})
            # Log en el sistema
            _logger = logging.getLogger(__name__)
            _logger.info(f'Cron: {len(tareas)} tareas vencidas canceladas automáticamente')