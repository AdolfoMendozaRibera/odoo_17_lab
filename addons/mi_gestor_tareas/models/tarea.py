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
    
    # 3. Las constraints SQL NO se pueden desactivar fácilmente:
       # Una vez creadas, son difíciles de modificar

       # Requieren migración de base de datos

       # Los constraints Python son más flexibles

    # ========== SQL CONSTRAINTS (CORREGIDOS) ==========
    #_sql_constraints = [
    #    # 1. Nombre único por usuario (más lógico)
    #    ('name_user_uniq', 
    #     'UNIQUE(name, create_uid)', 
    #     '¡Ya tienes una tarea con este nombre!'),
    #    
    #    # 2. Validación de prioridad
    #    ('prioridad_range_check',
    #     'CHECK(prioridad::integer BETWEEN 1 AND 5)',
    #     'La prioridad debe estar entre 1 y 5'),
    #    
    #    # 3. Fechas lógicas (Opcional - complementa la restricción Python)
    #    ('fecha_limite_check',
    #     'CHECK(fecha_limite IS NULL OR fecha_inicio IS NULL OR fecha_limite >= fecha_inicio)',
    #     'La fecha límite debe ser posterior a la fecha de inicio'),
    #]
    
    
    # ========== CAMPOS (COLUMNAS DE LA TABLA) ==========
    
    # Campo de texto simple (obligatorio)
    name = fields.Char(
        string='Nombre de la Tarea',  # Etiqueta que se muestra
        required=True,                 # No puede estar vacío
        tracking=True,
        help='Ingresa el nombre de tu tarea'  # Texto de ayuda
    )
    
    # Campo de texto largo (opcional)
    descripcion = fields.Text(
        string='Descripción',
        help='Descripción detallada de la tarea'
    )
    
    # Campo de fecha inicio
    fecha_inicio = fields.Date(
        string = 'Fecha de Inicio',
        required = True,
        default = fields.Date.context_today,
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
        ('pendiente', 'Pendiente'),      # (valor_interno, 'Texto que se muestra')
        ('en_progreso', 'En Progreso'),
        ('completada', 'Completada'),
    ], 
        string='Estado',
        default='borrador',  # Valor por defecto
        required=True,
          # <-- AÑADIDO: Permite traducción de los valores
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
          # <-- AÑADIDO: Permite traducción de los valores
    )
    

    # Campo calculado (se calcula automáticamente)
    dias_restantes = fields.Integer(
        string='Días Restantes',
        compute='_compute_dias_restantes',  # Función que lo calcula
        store=False  # No se guarda en BD, se calcula siempre
    )
    
    #
    # ========= BASE DE DATOS =============
    #CREATE TABLE mi_gestor_tareas_tarea (
    #    id SERIAL PRIMARY KEY,
    #    name VARCHAR NOT NULL,
    #    descripcion TEXT,
    #    fecha_limite DATE,
    #    estado VARCHAR,
    #    es_importante BOOLEAN,
    #    prioridad INTEGER,
    #    -- dias_restantes NO se guarda (se calcula)
    #);
    
    
    # ========== MÉTODOS (FUNCIONES) ==========
    
    # Método para calcular días restantes
    @api.depends('fecha_limite')  # Se recalcula cuando cambia fecha_limite
    def _compute_dias_restantes(self):
        hoy = date.today()
        # 'self' representa el registro actual (puede ser uno o varios)
        for tarea in self:
            if tarea.fecha_limite:
                delta = tarea.fecha_limite - hoy
                tarea.dias_restantes = delta.days
            else:
                tarea.dias_restantes = 0
    
    # Método que se ejecuta al hacer clic en un botón (lo veremos en la vista)
    def action_marcar_borrador(self):
        # Cambia el estado a borrador
        self.estado = 'borrador'
        return True
    
    def action_marcar_completada(self):
        # Cambia el estado a completada
        self.estado = 'completada'
        return True
    
    def action_marcar_pendiente(self):
        # Cambia el estado a pendiente
        self.estado = 'pendiente'
        return True
    
    def action_marcar_en_progreso(self):
        # Cambia el estado a en progreso
        self.estado = 'en_progreso'
        return True
    
    
    def action_imprimir_reporte(self):
        """Acción para imprimir reporte"""
        return self.env.ref('mi_gestor_tareas.action_report_tarea').report_action(self)
    
    
    
    # Restricciones
    
    @api.constrains('fecha_limite','fecha_inicio')
    def _check_fechas(self):
        for tarea in self:
            if tarea.fecha_limite and tarea.fecha_inicio:
                if tarea.fecha_limite < tarea.fecha_inicio:
                    raise models.ValidationError(
                        _("La fecha límite no puede ser anterior a la fecha de inicio.")
                    )
                
    """
    @api.constrains('prioridad')
    def _check_prioridad(self):
        for tarea in self:
            if tarea.prioridad and not tarea.prioridad.isDigit():
                raise models.ValidationError("La prioridad debe ser un número entre 1 y 5.")
    """
            
    @api.constrains('name')
    def _check_nombre(self):
        for tarea in self:
            if len(tarea.name.strip()) < 3:
                raise models.ValidationError(
                    _("El nombre de la tarea debe tener al menos 3 caracteres.")
                )
            
            if not tarea.name.strip():
                raise models.ValidationError(
                    _("El nombre de la tarea no puede estar vacío o contener solo espacios.")
                )