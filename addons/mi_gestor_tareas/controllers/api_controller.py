# -*- coding: utf-8 -*-

import json
from odoo import http
from odoo.http import request, Response

class TareaAPIController(http.Controller):
    
    @http.route('/api/tareas', type='http', auth='user', methods=['GET'])
    def obtener_tareas(self, **kwargs):
        """API para obtener tareas en formato JSON"""
        try:
            # Parámetros de filtro
            estado = kwargs.get('estado')
            importante = kwargs.get('importante')
            limite = int(kwargs.get('limite', 100))
            
            dominio = []
            if estado:
                dominio.append(('estado', '=', estado))
            if importante:
                dominio.append(('es_importante', '=', importante == 'true'))
            
            # Obtener tareas
            tareas = request.env['mi.gestor.tareas.tarea'].search_read(
                dominio,
                ['name', 'descripcion', 'estado', 'fecha_limite', 
                 'es_importante', 'prioridad', 'dias_restantes'],
                limit=limite
            )
            
            return Response(
                json.dumps({'success': True, 'data': tareas, 'total': len(tareas)}),
                content_type='application/json',
                status=200
            )
            
        except Exception as e:
            return Response(
                json.dumps({'success': False, 'error': str(e)}),
                content_type='application/json',
                status=500
            )
    
    @http.route('/api/tareas', type='json', auth='user', methods=['POST'])
    def crear_tarea_api(self, **kwargs):
        """API para crear una nueva tarea"""
        try:
            datos = request.jsonrequest
            
            nueva_tarea = request.env['mi.gestor.tareas.tarea'].create({
                'name': datos.get('nombre'),
                'descripcion': datos.get('descripcion'),
                'estado': datos.get('estado', 'pendiente'),
                'es_importante': datos.get('importante', False),
                'prioridad': datos.get('prioridad', '3'),
                'fecha_limite': datos.get('fecha_limite'),
            })
            
            return {
                'success': True,
                'id': nueva_tarea.id,
                'mensaje': 'Tarea creada exitosamente'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @http.route('/api/tareas/<int:tarea_id>', type='json', auth='user', methods=['PUT'])
    def actualizar_tarea_api(self, tarea_id, **kwargs):
        """API para actualizar una tarea"""
        try:
            tarea = request.env['mi.gestor.tareas.tarea'].browse(tarea_id)
            
            if not tarea.exists():
                return {'success': False, 'error': 'Tarea no encontrada'}
            
            datos = request.jsonrequest
            tarea.write(datos)
            
            return {
                'success': True,
                'mensaje': 'Tarea actualizada exitosamente'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}