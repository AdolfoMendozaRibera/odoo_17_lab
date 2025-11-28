# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Categoria(models.Model):
    """
    Modelo para categorías de tareas.
    Ejemplo: Trabajo, Personal, Urgente, etc.
    """
    
    # _name: Nombre técnico del modelo (así se llamará la tabla en PostgreSQL)
    # Formato: nombre_modulo.nombre_modelo (usa puntos, no guiones bajos)
    _name = 'mi_gestor_tareas.categoria'
    
    # _description: Descripción legible del modelo
    _description = 'Categoría de Tareas'
    
    # _order: Orden por defecto cuando se listen registros
    _order = 'nombre'
    
    # _rec_name: Campo que se usará como "nombre" del registro
    # Si no lo defines, Odoo busca automáticamente un campo llamado 'name'
    _rec_name = 'nombre'
    
    # ====================
    # CAMPOS DEL MODELO
    # ====================
    
    # Char: campo de texto corto (VARCHAR en SQL)
    # required=True: obligatorio al crear/guardar
    # String: etiqueta que se muestra en la interfaz
    nombre = fields.Char(
        string='Nombre de Categoría',
        required=True,
        help='Nombre descriptivo de la categoría'
    )
    
    # Text: campo de texto largo (TEXT en SQL)
    descripcion = fields.Text(
        string='Descripción'
    )
    
    # Selection: campo con opciones predefinidas (ENUM en SQL)
    color = fields.Selection([
        ('rojo', 'Rojo'),
        ('verde', 'Verde'),
        ('azul', 'Azul'),
        ('amarillo', 'Amarillo'),
    ], string='Color', default='azul')
    
    # Boolean: campo verdadero/falso
    activo = fields.Boolean(
        string='Activo',
        default=True,
        help='Desmarcar para archivar la categoría'
    )
    
    # One2many: relación "uno a muchos" (inversa de Many2one)
    # Esta categoría puede tener muchas tareas
    # Parámetros:
    #   1. Modelo relacionado
    #   2. Campo Many2one en el modelo relacionado que apunta a este modelo
    tarea_ids = fields.One2many(
        comodel_name='mi_gestor_tareas.tarea',
        inverse_name='categoria_id',
        string='Tareas'
    )
    
    # Integer: campo numérico entero
    # compute: el valor se calcula automáticamente con un método
    # store=True: guarda el valor en la BD (opcional, mejora rendimiento)
    total_tareas = fields.Integer(
        string='Total de Tareas',
        compute='_compute_total_tareas',
        store=True
    )
    
    # ====================
    # RESTRICCIONES SQL
    # ====================
    
    # Se aplican a nivel de base de datos
    # Son más rápidas y garantizan integridad de datos
    _sql_constraints = [
        # (nombre_constraint, regla_sql, mensaje_error)
        ('nombre_unico', 'UNIQUE(nombre)', 'Ya existe una categoría con ese nombre'),
    ]
    
    # ====================
    # MÉTODOS COMPUTE
    # ====================
    
    # @api.depends: indica qué campos deben cambiar para recalcular
    @api.depends('tarea_ids')
    def _compute_total_tareas(self):
        """
        Calcula el total de tareas de cada categoría.
        Este método se ejecuta automáticamente cuando:
        - Se crean/eliminan tareas asociadas
        - Se modifica tarea_ids
        """
        # self es un recordset (puede contener varios registros)
        # Por eso usamos 'for record in self'
        for record in self:
            # len() cuenta los registros en la relación One2many
            record.total_tareas = len(record.tarea_ids)
    
    # ====================
    # RESTRICCIONES PYTHON
    # ====================
    
    # @api.constrains: valida campos antes de guardar
    @api.constrains('nombre')
    def _check_nombre(self):
        """
        Valida que el nombre no esté vacío (aunque ya es required=True).
        Esto es un ejemplo didáctico de constraint.
        """
        for record in self:
            if record.nombre and len(record.nombre) < 3:
                raise ValidationError('El nombre debe tener al menos 3 caracteres')
    
    # ====================
    # HERENCIA DE MÉTODOS
    # ====================
    
    # Sobrescribimos el método create para agregar lógica personalizada
    @api.model
    def create(self, vals):
        """
        Se ejecuta al crear un nuevo registro.
        
        Args:
            vals (dict): Diccionario con los valores del nuevo registro
            
        Returns:
            record: El registro creado
        """
        # Ejemplo: convertir nombre a mayúsculas antes de crear
        if 'nombre' in vals:
            vals['nombre'] = vals['nombre'].upper()
        
        # SIEMPRE llamar a super() para ejecutar el create original
        # Si no lo haces, el registro no se creará en la BD
        return super(Categoria, self).create(vals)
    
    # Sobrescribimos write para agregar lógica al modificar
    def write(self, vals):
        """
        Se ejecuta al modificar registros existentes.
        
        Args:
            vals (dict): Diccionario con los campos a modificar
            
        Returns:
            bool: True si se guardó correctamente
        """
        # Ejemplo: también convertir a mayúsculas al editar
        if 'nombre' in vals:
            vals['nombre'] = vals['nombre'].upper()
        
        # Llamar al write original
        return super(Categoria, self).write(vals)
    
    # Sobrescribimos unlink para validar antes de eliminar
    def unlink(self):
        """
        Se ejecuta al eliminar registros.
        
        Returns:
            bool: True si se eliminó correctamente
        """
        # Validar: no permitir eliminar si tiene tareas asociadas
        for record in self:
            if record.tarea_ids:
                raise ValidationError(
                    f'No se puede eliminar la categoría "{record.nombre}" '
                    f'porque tiene {record.total_tareas} tarea(s) asociada(s)'
                )
        
        # Llamar al unlink original
        return super(Categoria, self).unlink()