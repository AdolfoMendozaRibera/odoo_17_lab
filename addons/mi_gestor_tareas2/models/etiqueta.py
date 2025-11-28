# -*- coding: utf-8 -*-
from odoo import models, fields

class Etiqueta(models.Model):
    """
    Modelo para etiquetas de tareas.
    Ejemplo: #urgente, #revisar, #importante
    Relación Many2many con tareas (una tarea puede tener varias etiquetas,
    una etiqueta puede estar en varias tareas)
    """
    
    _name = 'mi_gestor_tareas.etiqueta'
    _description = 'Etiqueta de Tarea'
    _order = 'nombre'
    
    # ====================
    # CAMPOS
    # ====================
    
    nombre = fields.Char(
        string='Nombre',
        required=True
    )
    
    # Integer: número de 0-11 para colorear en vista kanban
    color = fields.Integer(
        string='Color Index',
        default=0
    )
    
    # Many2many: relación muchos a muchos
    # Una etiqueta puede estar en muchas tareas
    # Una tarea puede tener muchas etiquetas
    tarea_ids = fields.Many2many(
        comodel_name='mi_gestor_tareas.tarea',
        # relation: nombre de la tabla intermedia (opcional)
        # Si no lo defines, Odoo crea uno automático
        relation='tarea_etiqueta_rel',
        # column1: columna para este modelo en la tabla intermedia
        column1='etiqueta_id',
        # column2: columna para el otro modelo
        column2='tarea_id',
        string='Tareas'
    )
    
    # ====================
    # RESTRICCIONES
    # ====================
    
    _sql_constraints = [
        ('nombre_unico', 'UNIQUE(nombre)', 'Ya existe una etiqueta con ese nombre'),
    ]