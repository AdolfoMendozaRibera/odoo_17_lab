import xmlrpc.client

# 1. Configuración: Estos son tus "credenciales de acceso".
url = 'http://localhost:8069' 
db = 'odoo18_lab'
username = 'Usuario_API'
# El password es el API Key, que es más seguro que usar tu clave real.
password = '0379acbaaf62e052075de20f7e7e2a0fc6639406'

# 2. El endpoint 'common' sirve para servicios generales (login, versión).
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
print("Versión de Odoo:", common.version())

# 3. Autenticación: Si los datos son correctos, Odoo te da un entero (UID).
# Sin este UID no puedes hacer nada en los siguientes pasos.
uid = common.authenticate(db, username, password, {})
print('Tu ID de usuario es: ', uid)

# 4. El endpoint 'object' es el que permite "hablar" con los modelos (Tablas).
# Nota: Quité un espacio en blanco que tenías en la URL para evitar errores.
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# --- EXPLICACIÓN DE EXECUTE_KW ---
# Es el "traductor". Envía tu petición al servidor de Odoo.
# La estructura siempre es: (DB, UID, PASS, MODELO, MÉTODO, POSICIONALES, NOMBRADOS)

# EJEMPLO 1: Llamar a una función de un botón.
# Esto simula que un usuario hizo clic en el botón "Pasar a Borrador" en una compra.
# [[18]] es el ID de la orden de compra.
# result_button_draft = models.execute_kw(db, uid, password, 'purchase.order', 'button_draft', [[18]])

# EJEMPLO 2: Método 'read' (Lectura)
# Trae todos los campos del contacto con ID 101.
result_execute = models.execute_kw(db, uid, password, 'res.partner','read', [[101]]) 
print("Datos completos del contacto:", result_execute)

# EJEMPLO 3: Lectura filtrada (Optimización)
# En una API es mejor pedir solo lo que necesitas para no saturar la red.
# El diccionario {'fields': [...]} limita las columnas que Odoo devuelve.
result_execute = models.execute_kw(db, uid, password, 'res.partner','read', [[101]], 
                                   {'fields': ['name', 'country_id', 'comment']}) 
print("Campos específicos:", result_execute)

# --- ACCIONES DE ARCHIVADO ---
# Muy útil para "borrar" lógicamente (sin eliminar de la DB) registros médicos o clientes.
try:
    # OJO: corregí 'action archive' por 'action_archive' (con guion bajo).
    # Odoo usa guiones bajos para los nombres de métodos.
    models.execute_kw(db, uid, password, 'res.partner', 'action_archive', [[66, 52]])
    print("Registros archivados correctamente.")
except xmlrpc.client.Fault as e:
    # El objeto 'Fault' captura errores de lógica de Odoo (ej: no tienes permiso).
    print("Error de Odoo:", e.faultString)
except Exception as e:
    # Captura errores de conexión (ej: el Docker está apagado).
    print("Error de conexión:", e)


"""
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')


uid = common.authenticate(db, username, password, {})

if uid:
    print(f"¡Conexión exitosa! ID de usuario: {uid}")
    
    # 3. Preparar el túnel para enviar órdenes (execute_kw)
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

    # EJEMPLO: Leer los nombres de los primeros 5 pacientes de oeHealth
    # (Asumiendo que el modelo de oeHealth se llama oeh.medical.patient)
    pacientes = models.execute_kw(db, uid, password,
        'res.partner', 'search_read', # Uso 'res.partner' porque es el estándar de contactos
        [[]], # Filtros (vacío = todos)
        {'fields': ['name', 'email'], 'limit': 5} # Campos que quiero traer
    )

    print("Listado de Pacientes/Contactos:")
    for p in pacientes:
        print(f"- {p['name']} ({p.get('email', 'Sin correo')})")
else:
    print("Error de autenticación.")

"""