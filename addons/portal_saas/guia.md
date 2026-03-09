Necesito ayuda con un problema técnico en Odoo 17 usando Docker.

Contexto del entorno

Sistema operativo: Windows 10

Uso: Docker Desktop + Docker Compose

Tengo un contenedor principal con Odoo 17 (lo llamo “Odoo maestro”)

Desde el maestro puedo crear, activar y desactivar nuevas instancias Odoo dinámicamente (arquitectura tipo SaaS).

He desarrollado/mejorado un módulo personalizado que se enfoca en la creación automática de nuevas instancias.

Problema

Cuando creo una nueva instancia llamada "hola", esta se genera correctamente con su propia estructura de carpetas y docker-compose.

En la sección de repositorios del sistema maestro:

Agrego la URL de mi repositorio

Indico la rama correspondiente

El repositorio contiene dos módulos:

hospital

odoo_web

La instancia se crea correctamente y los módulos físicamente sí se copian al contenedor.

Sin embargo:

Entro a la nueva instancia "hola"

Activo modo desarrollador

Actualizo la lista de aplicaciones

Busco el módulo hospital

❌ No aparece

Pero los módulos SÍ existen físicamente dentro del contenedor.

Verificación en sistema de archivos

Ruta donde se crean las instancias:

/d/odoo_lab/odoo17_Dev/odoo_data/odoo_docker/data/hola/

Estructura:

hola/
 ├── addons/
 │    └── odoo_17_lab_branch_prueba/
 ├── docker-compose.yml
 └── etc/

El módulo está dentro de:

hola/addons/odoo_17_lab_branch_prueba/
docker-compose.yml de la instancia "hola"
services:
  db:
    image: postgres:15
    environment:
      - POSTGRES_PASSWORD=odoo
      - POSTGRES_USER=odoo
      - POSTGRES_DB=postgres
    restart: unless-stopped
    volumes:
      - ./postgresql:/var/lib/postgresql/data

  odoo17:
    image: odoo:17
    user: root
    depends_on:
      - db
    ports:
      - "8073:8069"
      - "8074:8072"
    tty: true
    command: --
    environment:
      - HOST=db
      - USER=odoo
      - PASSWORD=odoo
    volumes:
      - ./addons:/mnt/extra-addons
      - ./etc:/etc/odoo
      - ./data:/var/lib/odoo
    restart: unless-stopped

    
etc/odoo.conf de la instancia
[options]
db_maxconn = 64
proxy_mode = True
addons_path = /usr/lib/python3/dist-packages/odoo/addons,{{ADDONS_PATH}}
admin_passwd = admin
data_dir = /var/lib/odoo
db_host = {{DB_HOST}}
db_user = {{DB_USER}}
db_password = {{DB_PASSWORD}}
db_port = 5432
Información importante

En mi Odoo maestro SÍ funciona correctamente. Allí el addons_path está configurado así:

addons_path = /mnt/extra-addons/oehealth_original,
/mnt/extra-addons/oehealth_extensiones,
/mnt/extra-addons/oehealth_mis_extensiones,
/mnt/extra-addons/portal_saas,
/usr/lib/python3/dist-packages/odoo/addons

Y en el docker-compose del maestro tengo:

volumes:
  - ./addons:/mnt/extra-addons
Lo que necesito

Que la nueva instancia detecte correctamente los módulos que están en ./addons.

Que aparezcan al actualizar la lista de aplicaciones.

Que la solución sea persistente (que funcione aunque reinicie o detenga los contenedores).

Que la configuración sea adecuada para un entorno donde estaré creando múltiples instancias dinámicamente.

Lo que quiero que analices

Si el problema es del addons_path

Si el placeholder {{ADDONS_PATH}} no está siendo reemplazado

Si el volumen no está mapeando correctamente

Si Odoo necesita permisos específicos

Si el command: -- está afectando el arranque

Si la estructura de carpetas impide que Odoo detecte los módulos

Qué configuración debería tener para arquitectura SaaS con múltiples instancias dinámicas

Necesito una solución técnica clara, explicando:

La causa exacta

Qué modificar

Ejemplo corregido de docker-compose.yml

Ejemplo corregido de odoo.conf

Buenas prácticas para este tipo de arquitectura