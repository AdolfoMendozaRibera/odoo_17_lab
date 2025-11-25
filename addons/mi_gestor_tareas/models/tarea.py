# -*- coding: utf-8 -*-

from odoo import models, fields, api

# Esta clase define el modelo de datos (la tabla en la base de datos)
class Tarea(models.Model):
    # _name: nombre técnico del modelo (se convierte en tabla: mi_gestor_tareas_tarea)
    _name = 'mi.gestor.tareas.tarea'
    
    # _description: descripción del modelo
    _description = 'Tarea Personal'
    
    # _order: cómo se ordenan los registros por defecto
    _order = 'fecha_limite desc, name'
    
    
    # ========== CAMPOS (COLUMNAS DE LA TABLA) ==========
    
    # Campo de texto simple (obligatorio)
    name = fields.Char(
        string='Nombre de la Tarea',  # Etiqueta que se muestra
        required=True,                 # No puede estar vacío
        help='Ingresa el nombre de tu tarea'  # Texto de ayuda
    )
    
    # Campo de texto largo (opcional)
    descripcion = fields.Text(
        string='Descripción',
        help='Descripción detallada de la tarea'
    )
    
    # Campo de fecha
    fecha_limite = fields.Date(
        string='Fecha Límite',
        help='¿Cuándo debe estar lista?'
    )
    
    # Campo de selección (como un dropdown)
    estado = fields.Selection([
        ('pendiente', 'Pendiente'),      # (valor_interno, 'Texto que se muestra')
        ('en_progreso', 'En Progreso'),
        ('completada', 'Completada'),
    ], 
        string='Estado',
        default='pendiente',  # Valor por defecto
        required=True
    )
    
    # Campo booleano (checkbox)
    es_importante = fields.Boolean(
        string='¿Es Importante?',
        default=False
    )
    
    # Campo numérico entero
    prioridad = fields.Integer(
        string='Prioridad',
        default=1,
        help='1=Baja, 2=Media, 3=Alta'
    )
    
    # Campo calculado (se calcula automáticamente)
    dias_restantes = fields.Integer(
        string='Días Restantes',
        compute='_compute_dias_restantes',  # Función que lo calcula
        store=False  # No se guarda en BD, se calcula siempre
    )
    
    
    # ========== MÉTODOS (FUNCIONES) ==========
    
    # Método para calcular días restantes
    @api.depends('fecha_limite')  # Se recalcula cuando cambia fecha_limite
    def _compute_dias_restantes(self):
        # 'self' representa el registro actual (puede ser uno o varios)
        for tarea in self:
            if tarea.fecha_limite:
                # Calcula la diferencia entre fecha límite y hoy
                from datetime import date
                hoy = date.today()
                delta = tarea.fecha_limite - hoy
                tarea.dias_restantes = delta.days
            else:
                tarea.dias_restantes = 0
    
    # Método que se ejecuta al hacer clic en un botón (lo veremos en la vista)
    def action_marcar_completada(self):
        # Cambia el estado a completada
        for tarea in self:
            tarea.estado = 'completada'
    
    # Método para marcar como pendiente
    def action_marcar_pendiente(self):
        for tarea in self:
            tarea.estado = 'pendiente'