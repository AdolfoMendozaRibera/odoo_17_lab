import click
from odoo import api, fields, models, _

class TareaCommands(models.AbstractModel):
    _name = 'tarea.commands'
    _description = 'Comandos CLI para gestión de tareas'
    
    def ejecutar_comando(self, comando, parametros=None):
        """Ejecuta comandos desde la línea de comandos"""
        if comando == 'crear_masivo':
            return self.crear_tareas_masivas(int(parametros.get('cantidad', 5)))
        elif comando == 'estadisticas':
            return self.obtener_estadisticas()
        elif comando == 'limpiar_completadas':
            return self.limpiar_tareas_completadas()
        return {'error': 'Comando no reconocido'}
    
    def crear_tareas_masivas(self, cantidad=5):
        """Crea tareas de prueba"""
        for i in range(cantidad):
            self.env['mi.gestor.tareas.tarea'].create({
                'name': f'Tarea de prueba {i+1}',
                'descripcion': f'Tarea creada automáticamente #{i+1}',
                'estado': 'pendiente',
                'prioridad': str((i % 5) + 1)
            })
        return {'mensaje': f'Se crearon {cantidad} tareas de prueba'}
    
    def obtener_estadisticas(self):
        """Obtiene estadísticas de tareas"""
        Tarea = self.env['mi.gestor.tareas.tarea']
        return {
            'total': Tarea.search_count([]),
            'pendientes': Tarea.search_count([('estado', '=', 'pendiente')]),
            'completadas': Tarea.search_count([('estado', '=', 'completada')]),
            'importantes': Tarea.search_count([('es_importante', '=', True)]),
        }
    
    def limpiar_tareas_completadas(self):
        """Elimina tareas completadas antiguas"""
        tareas = self.env['mi.gestor.tareas.tarea'].search([
            ('estado', '=', 'completada'),
            ('write_date', '<', fields.Date.today())
        ])
        count = len(tareas)
        tareas.unlink()
        return {'mensaje': f'Se eliminaron {count} tareas completadas'}