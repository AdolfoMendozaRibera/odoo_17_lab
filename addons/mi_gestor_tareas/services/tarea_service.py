# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta

class TareaService(models.Model):
    _name = 'tarea.service'
    _description = 'Servicio de gestión de tareas'
    
    # No necesitamos campos, es un servicio
    
    # ========== MÉTODOS DE SERVICIO ==========
    
    def crear_tarea_rapida(self, nombre, usuario_id=None):
        """Crea una tarea rápida con valores por defecto"""
        valores = {
            'name': nombre,
            'estado': 'pendiente',
            'fecha_inicio': fields.Date.today(),
            'fecha_limite': fields.Date.today() + timedelta(days=7),
            'prioridad': '3',
        }
        
        if usuario_id:
            valores['user_id'] = usuario_id
            
        return self.env['mi.gestor.tareas.tarea'].create(valores)
    
    def obtener_tareas_por_usuario(self, usuario_id):
        """Obtiene todas las tareas de un usuario específico"""
        return self.env['mi.gestor.tareas.tarea'].search([
            ('create_uid', '=', usuario_id)
        ])
    
    def completar_todas_pendientes(self, usuario_id=None):
        """Marca como completadas todas las tareas pendientes"""
        dominio = [('estado', '=', 'pendiente')]
        
        if usuario_id:
            dominio.append(('create_uid', '=', usuario_id))
            
        tareas_pendientes = self.env['mi.gestor.tareas.tarea'].search(dominio)
        tareas_pendientes.write({'estado': 'completada'})
        
        return len(tareas_pendientes)
    
    def obtener_estadisticas(self):
        """Obtiene estadísticas de las tareas"""
        total = self.env['mi.gestor.tareas.tarea'].search_count([])
        
        estadisticas = {
            'total': total,
            'pendientes': self.env['mi.gestor.tareas.tarea'].search_count([
                ('estado', '=', 'pendiente')
            ]),
            'completadas': self.env['mi.gestor.tareas.tarea'].search_count([
                ('estado', '=', 'completada')
            ]),
            'importantes': self.env['mi.gestor.tareas.tarea'].search_count([
                ('es_importante', '=', True)
            ]),
            'vencidas': self.env['mi.gestor.tareas.tarea'].search_count([
                ('fecha_limite', '<', fields.Date.today()),
                ('estado', '!=', 'completada')
            ]),
        }
        
        estadisticas['porcentaje_completado'] = (
            (estadisticas['completadas'] / total * 100) if total > 0 else 0
        )
        
        return estadisticas
    
    def duplicar_tarea(self, tarea_id):
        """Duplica una tarea existente"""
        tarea_original = self.env['mi.gestor.tareas.tarea'].browse(tarea_id)
        
        if not tarea_original.exists():
            return False
            
        valores_duplicado = tarea_original.copy_data({
            'name': f"Copia de {tarea_original.name}",
            'estado': 'borrador'
        })[0]
        
        return self.env['mi.gestor.tareas.tarea'].create(valores_duplicado)