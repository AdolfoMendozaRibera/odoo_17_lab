import sys
import os

# Agregar el path de Odoo
sys.path.append('/usr/lib/python3/dist-packages')

# Inicializar Odoo
import odoo
from odoo import api, fields, models
from odoo.tools import config

# Configurar
config.parse_config(['-c', '/etc/odoo/odoo.conf', '-d', 'odoo17'])

# Inicializar Odoo
odoo.tools.config.parse_config([])
registry = odoo.modules.registry.Registry.new('odoo17')
with registry.manage_changes():
    cr = registry.cursor()
    env = api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    try:
        # Verificar si existe el modelo
        if 'tarea.commands' in env:
            print("✅ Modelo 'tarea.commands' encontrado")
            
            # Usar tu servicio
            service = env['tarea.commands']
            
            # Probar comandos
            print("\n📊 Obteniendo estadísticas...")
            stats = service.obtener_estadisticas()
            print(f"   Total tareas: {stats.get('total', 0)}")
            print(f"   Pendientes: {stats.get('pendientes', 0)}")
            print(f"   Completadas: {stats.get('completadas', 0)}")
            print(f"   Importantes: {stats.get('importantes', 0)}")
            
            print("\n➕ Creando tarea de prueba...")
            Tarea = env['mi.gestor.tareas.tarea']
            nueva_tarea = Tarea.create({
                'name': 'Tarea creada desde API',
                'descripcion': 'Esta tarea fue creada automáticamente',
                'estado': 'pendiente',
                'prioridad': '4'
            })
            print(f"   ✅ Tarea creada: ID {nueva_tarea.id}, Nombre: {nueva_tarea.name}")
            
            cr.commit()
        else:
            print("❌ Modelo 'tarea.commands' NO encontrado")
            print("   Verifica que tu módulo esté instalado")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        cr.rollback()
    finally:
        cr.close()
