# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date
from odoo.tools.translate import _


# Esta clase define el modelo de datos (la tabla en la base de datos)
class Tarea(models.Model):
    # _name: nombre técnico del modelo (se convierte en tabla: mi_gestor_tareas_tarea)
    _name = 'mi.gestor.tareas.tarea'
    
    # Hereda funcionalidades de seguimiento de mensajes
    _inherit = ['mail.thread','mail.activity.mixin']  
    
    # _description: descripción del modelo
    _description = 'Tarea Personal'
    
    # _order: cómo se ordenan los registros por defecto
    _order = 'fecha_limite desc, name asc'
    
    # ========== CAMPOS (COLUMNAS DE LA TABLA) ==========
    
    # Campo de texto simple (obligatorio)
    name = fields.Char(
        string='Nombre de la Tarea',
        required=True,
        tracking=True,
        help='Ingresa el nombre de tu tarea'
    )
    
    # Campo de texto largo (opcional)
    descripcion = fields.Text(
        string='Descripción',
        help='Descripción detallada de la tarea'
    )
    
    # Campo de fecha inicio
    fecha_inicio = fields.Date(
        string='Fecha de Inicio',
        required=True,
        default=fields.Date.context_today,
        help='Cuando comenzo la tarea',
    )
    
    # Campo de fecha
    fecha_limite = fields.Date(
        string='Fecha Límite',
        help='¿Cuándo debe estar lista?'
    )
    
    # Campo de selección (como un dropdown)
    estado = fields.Selection([
        ('borrador', 'Borrador'),
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En Progreso'),
        ('completada', 'Completada'),
    ], 
        string='Estado',
        default='borrador',
        required=True,
    )
    
    # Campo booleano (checkbox)
    es_importante = fields.Boolean(
        string='¿Es Importante?',
        default=False
    )
    
    # Campo numérico entero
    prioridad = fields.Selection(
        selection=[
            ('1', 'Muy Baja'),
            ('2', 'Baja'),
            ('3', 'Media'),
            ('4', 'Alto'),
            ('5', 'Muy Alto'),
        ],
        string='Prioridad',
        help='Nivel de prioridad de la tarea',
        default='3',
    )
    
    # Campo calculado (se calcula automáticamente)
    dias_restantes = fields.Integer(
        string='Días Restantes',
        compute='_compute_dias_restantes',
        store=False
    )
    
    # ========== MÉTODOS (FUNCIONES) ==========
    
    # Método para calcular días restantes
    @api.depends('fecha_limite')
    def _compute_dias_restantes(self):
        hoy = date.today()
        for tarea in self:
            if tarea.fecha_limite:
                delta = tarea.fecha_limite - hoy
                tarea.dias_restantes = delta.days
            else:
                tarea.dias_restantes = 0
    
    # Métodos helpers para usar en cualquier lugar
    def get_estado_traducido(self):
        """Retorna el estado traducido según el idioma actual"""
        if not self.estado:
            return ''
        return dict(self._fields['estado'].selection).get(self.estado, self.estado)
    
    def get_prioridad_traducida(self):
        """Retorna la prioridad traducida según el idioma actual"""
        if not self.prioridad:
            return ''
        return dict(self._fields['prioridad'].selection).get(self.prioridad, self.prioridad)
    
    # Métodos de acción
    def action_marcar_borrador(self):
        """Cambia el estado a borrador"""
        self.estado = 'borrador'
        return True
    
    def action_marcar_completada(self):
        """Cambia el estado a completada"""
        self.estado = 'completada'
        return True
    
    def action_marcar_pendiente(self):
        """Cambia el estado a pendiente"""
        self.estado = 'pendiente'
        return True
    
    def action_marcar_en_progreso(self):
        """Cambia el estado a en progreso"""
        self.estado = 'en_progreso'
        return True
    
    def action_imprimir_reporte(self):
        """Acción para imprimir reporte"""
        return self.env.ref('mi_gestor_tareas.action_report_tarea').report_action(self)
    
    # ========== RESTRICCIONES ==========
    
    @api.constrains('fecha_limite', 'fecha_inicio')
    def _check_fechas(self):
        """Valida que la fecha límite no sea anterior a la fecha de inicio"""
        for tarea in self:
            if tarea.fecha_limite and tarea.fecha_inicio:
                if tarea.fecha_limite < tarea.fecha_inicio:
                    raise models.ValidationError(
                        _("La fecha límite no puede ser anterior a la fecha de inicio.")
                    )
    
    @api.constrains('name')
    def _check_nombre(self):
        """Valida que el nombre tenga al menos 3 caracteres y no esté vacío"""
        for tarea in self:
            if len(tarea.name.strip()) < 3:
                raise models.ValidationError(
                    _("El nombre de la tarea debe tener al menos 3 caracteres.")
                )
            
            if not tarea.name.strip():
                raise models.ValidationError(
                    _("El nombre de la tarea no puede estar vacío o contener solo espacios.")
                )