# OeHealth Custom Appointments

## 📋 Descripción General

**OeHealth Custom Appointments** es un módulo de extensión para **Odoo 17** que amplía significativamente la funcionalidad de gestión de citas médicas en el sistema **OeHealth**.

Este módulo añade nuevos estados de citas, tipos de citas, funcionalidades de reprogramación, y reportes analíticos avanzados para mejorar la experiencia de gestión de pacientes y citas en centros de salud.

---

## 🎯 Características Principales

### 1. **Estados Mejorados de Citas**
```
├── Scheduled (Programada)    → Azul Info
├── Completed (Realizada)     → Verde Success
├── Reprogramada              → Amarillo Warning
├── Sin Asistir               → Rojo Danger
└── Invoiced (Facturada)      → Gris Muted
```

### 2. **Gestión de Tipos de Cita**
- Campo `appointment_type` para clasificar citas
- Permite diferenciar entre tipos de consultas
- Utilizado en reportes y análisis

### 3. **Botones de Acciones Personalizados**
- ✓ **Marcar como Realizado** - Completa la cita
- 💳 **Facturado** - Marca como facturada
- ✗ **Sin Asistir** - Registra inasistencia
- ↻ **Reprogramar** - Abre wizard para reprogramar

### 4. **Wizard de Reprogramación**
```
Permite:
├── Seleccionar nueva fecha/hora
├── Agregar notas sobre la reprogramación
└── Crear cita relacionada automáticamente
```

### 5. **Reportes Analíticos**
- **Reporte de Asistencia** - Gráfico de barras por estado
- **Reporte por Tipo de Cita** - Gráfico de pastel por demanda

### 6. **Filtros Temporales Avanzados**
```
├── Hoy
├── Esta Semana
├── Este Mes
└── Este Año
```

### 7. **Vistas Múltiples**
```
├── Form (Formulario detallado)
├── Tree (Lista con colores)
├── Calendar (Calendario con código de colores)
└── Graph (Gráficos de análisis)
```

---

## 📁 Estructura del Módulo

```
module_patients_citas/
├── __init__.py                          
├── __manifest__.py                      
├── models/
│   ├── __init__.py
│   ├── appointment.py                   
│   └── appointment_wizard.py            
├── views/
│   ├── appointment_view.xml             
│   └── appointment_reprogramar_wizard_view.xml  
├── security/
│   └── ir.model.access.csv              
├── static/src/css/
│   └── oehealth_calendar_colors.css     
└── README.md                            
```

---

## 🔧 Información Técnica

### **Versión**
```
Versión: 17.0.1.0.0
Categoría: Healthcare
Licencia: LGPL-3
Odoo Requerido: 17.0+
Autor: Ronald-Ribentek
```

### **Dependencias**
```python
'depends': [
    'oehealth',                    # Base de OeHealth
    'module_roles_oehealth',       # Módulo de roles personalizado
],
```

### **Modelos Extendidos**
- `oeh.medical.appointment` - Citas médicas extendidas
- `appointment.reprogramar.wizard` - Wizard para reprogramación

### **Vistas Definidas**

| Vista | Tipo | Propósito |
|-------|------|----------|
| `oeh_medical_appointment_custom_form` | Form | Formulario detallado de cita |
| `oeh_medical_appointment_custom_tree` | Tree | Lista con código de colores |
| `oeh_medical_appointment_custom_calendar` | Calendar | Calendario interactivo |
| `view_oeh_medical_appointment_graph_custom` | Graph | Análisis de asistencia (barras) |
| `view_oeh_medical_appointment_graph_demand` | Graph | Análisis de demanda (pastel) |
| `view_oeh_medical_appointment_filter_custom` | Search | Filtros avanzados |
| `appointment_reprogramar_wizard_form` | Form | Wizard de reprogramación |

---

## 🎨 Sistema de Colores

### Vista Lista, Árbol y Calendario

```
┌─────────────────────────────────────────────────┐
│ Estado                    Color         Código  │
├─────────────────────────────────────────────────┤
│ Scheduled (Programada)    Azul Info     #0dcaf0│
│ Completed (Realizada)     Verde         #28a745│
│ Reprogramada              Amarillo      #ffc107│
│ Sin Asistir               Rojo          #dc3545│
│ Invoiced (Facturada)      Gris          #6c757d│
└─────────────────────────────────────────────────┘
```

**Archivo CSS personalizado:** `oehealth_calendar_colors.css`
- Sincroniza colores entre vistas
- Estilos hover mejorados
- Sombras y efectos visuales
- Oculta filtro de color en sidebar

---

## 👥 Control de Acceso por Roles

### Matriz de Permisos

| Rol | Crear | Leer | Editar | Eliminar | Acciones | Reportes |
|-----|-------|------|--------|----------|----------|----------|
| **Administrator** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Physician (Médico)** | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ |
| **Receptionist** | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ |
| **Manager** | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |

*Nota: Los permisos específicos se definen en `security/ir.model.access.csv`*

---

## 📊 Reportes Disponibles

### **1. Reporte de Asistencia**
```
Tipo:           Gráfico de Barras
Datos:          Conteo de estados de citas
Dimensión:      Estados (Scheduled, Completed, etc.)
Filtro Defecto: Este mes
Agrupación:     Por Estado
Uso:            Analizar patrones de asistencia
```

### **2. Reporte por Tipo de Cita**
```
Tipo:           Gráfico de Pastel
Datos:          Distribución de tipos de cita
Dimensión:      Tipo de Cita
Filtro Defecto: Este mes
Excluye:        Citas sin asistir
Uso:            Entender demanda por especialidad
```

---

## 🚀 Instalación

### **Requisitos Previos**
- Odoo 17.0+
- Módulo `oehealth` instalado
- Módulo `module_roles_oehealth` instalado

### **Paso 1: Verificar ubicación**
```bash
ls -la odoo17/addons/module_for_oehealth/module_patients_citas/
```

### **Paso 2: Actualizar lista de aplicaciones**
1. Ve a **Aplicaciones** en Odoo
2. Haz clic en **Actualizar** (arriba a la derecha)
3. Espera a que termine

### **Paso 3: Instalar el módulo**
1. Busca: `OeHealth Custom Appointments`
2. Haz clic en **Instalar**
3. Espera a que se complete

### **Paso 4: Verificar instalación**
- Aparecerá en **Aplicaciones Instaladas**
- Deberías ver nuevas opciones en **Citas generales**

---

## 📱 Guía de Uso

### **Crear una Nueva Cita**
```
1. Ve a Citas generales → Citas
2. Haz clic en "Nuevo"
3. Completa los campos requeridos:
   ✓ Paciente (requerido)
   ✓ Tipo de Cita (requerido)
   - Médico (opcional)
   - Fecha y hora
4. Guarda con Ctrl + S o haz clic en "Guardar"
```

### **Marcar Cita como Realizada**
```
1. Abre la cita en estado "Scheduled"
2. Haz clic en botón "✓ Marcar como Realizado"
3. Estado cambia automáticamente a "Completed"
4. Se guarda sin confirmar
```

### **Registrar Inasistencia**
```
1. Abre la cita en estado "Scheduled"
2. Haz clic en botón "✗ Sin Asistir"
3. Estado cambia a "Sin Asistir"
4. Se guarda automáticamente
Nota: Las citas con inasistencia no se incluyen en ciertos reportes
```

### **Reprogramar una Cita**
```
1. Abre la cita en estado "Scheduled"
2. Haz clic en botón "↻ Reprogramar"
3. Se abre wizard con estos campos:
   - Nueva fecha/hora (requerido)
   - Notas de reprogramación (opcional)
4. Haz clic en "Reprogramar"
5. Resultado:
   ✅ Se crea nueva cita con los datos originales
   ✅ Cita original marca como "Reprogramada"
   ✅ Se vinculan automáticamente (parent_appointment_id)
```

### **Generar Factura**
```
Opción 1: Desde la Cita
  1. Abre cita en estado "Completed"
  2. Haz clic en "💳 Facturado"
  3. Se genera factura automáticamente

Opción 2: Desde el botón "Create Invoice"
  Tipo de facturación:
  - Solo por consulta (consulta médica)
  - Solo para items (tratamientos, recetas, exámenes)
  - Ambos (consulta + items)
```

### **Ver Reportes**
```
Reporte de Asistencia:
  Menú → Citas generales → Reporte de Asistencia
  - Gráfico de barras
  - Filtra por período (Este mes por defecto)

Reporte por Tipo de Cita:
  Menú → Citas generales → Reporte por Tipo de Cita
  - Gráfico de pastel
  - Muestra distribución de demanda
```

---

## 🔍 Filtros y Búsqueda

### Campos de Búsqueda
```
├── Nombre de cita
├── Nombre del paciente
├── Tipo de cita
└── Fecha de cita
```

### Filtros Rápidos Predefinidos
```
├── Hoy              → Citas de hoy
├── Esta Semana      → Citas de la semana actual
├── Este Mes         → Citas del mes actual
└── Este Año         → Citas del año actual
```

### Agrupación
```
├── Por Paciente
├── Por Estado
├── Por Médico
└── Por Tipo de Cita
```

---

## 📝 Campos del Modelo

### `oeh.medical.appointment` (Extendido)

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-----------|
| `name` | Char | ✓ | ID único de la cita (readonly) |
| `patient_id` | Many2one | ✓ | Paciente |
| `physician_id` | Many2one | - | Médico asignado |
| `appointment_date` | DateTime | ✓ | Fecha y hora de cita |
| `appointment_type` | Selection | ✓ | Tipo de cita |
| `state` | Selection | - | Estado (Scheduled, Completed, etc.) |
| `duration` | Float | - | Duración en horas |
| `notes` | Text | - | Notas clínicas |
| `parent_appointment_id` | Many2one | - | Cita original (si reprogramada) |
| `move_id` | Many2one | - | Factura relacionada |
| `color` | Integer | - | Color para calendario |

### `appointment.reprogramar.wizard`

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-----------|
| `appointment_id` | Many2one | ✓ | Cita a reprogramar |
| `new_date` | DateTime | ✓ | Nueva fecha/hora |
| `notes` | Text | - | Motivo de reprogramación |

---

## 🛠️ Personalización

### **Modificar un Campo en el Formulario**

Archivo: `views/appointment_view.xml`

```xml
<xpath expr="//field[@name='notes']" position="attributes">
    <attribute name="required">true</attribute>
    <attribute name="placeholder">Ingrese observaciones aquí</attribute>
</xpath>
```

### **Agregar un Nuevo Botón**

```xml
<xpath expr="//button[@name='set_to_completed']" position="after">
    <button name="action_custom" type="object" 
            string="Mi Botón Personalizado"
            class="btn-primary"/>
</xpath>
```

### **Cambiar Colores en el Calendario**

Archivo: `static/src/css/oehealth_calendar_colors.css`

```css
/* Cambiar color de citas programadas */
.o_calendar_renderer .o_calendar_event.o_calendar_color_4 {
    background-color: #0dcaf0 !important;
    border-color: #0a58ca !important;
}
```

### **Agregar Filtro Personalizado**

```xml
<xpath expr="//filter[@name='filter_month']" position="after">
    <filter name="mi_filtro" string="Mi Filtro"
            domain="[('state', '=', 'completed')]"/>
</xpath>
```

---

## 📋 Estados de Cita - Flujo de Estados

```
                    ┌─────────────────┐
                    │   Scheduled     │
                    │  (Programada)   │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
    ┌─────────┐      ┌──────────────┐     ┌──────────┐
    │Completed│      │Reprogramada  │     │Sin Asistir
    │(Realiza)│      │              │     │          │
    └────┬────┘      └──────────────┘     └──────────┘
         │
         ▼
    ┌─────────┐
    │ Invoiced│
    │(Factura)│
    └─────────┘
```

---

## 🐛 Solución de Problemas

### **Los botones de acciones no se muestran**
```
✓ Verifica que el usuario tenga rol correcto
✓ Ve a Ajustes → Usuarios → Tu usuario
✓ Confirma que está en rol: Physician o Receptionist
✓ Limpia caché: Ctrl + Shift + Delete
```

### **Colores no coinciden entre vistas**
```
✓ Verifica CSS cargado: Ajustes → Modo Desarrollador → Información de Vista
✓ Recarga página completa: F5 o Ctrl + F5
✓ Limpia caché del navegador
```

### **Reportes sin datos**
```
✓ Verifica que haya citas en el rango de fechas
✓ Aplica el filtro temporal correcto
✓ Comprueba que las citas tengan estado válido
✓ Excluye citas "Sin Asistir" si es necesario
```

### **Wizard de reprogramación no funciona**
```
✓ Verifica que la cita esté en estado "Scheduled"
✓ Confirma que hay disponibilidad en nueva fecha
✓ Verifica permisos: debe poder crear citas
```

### **La factura no se genera**
```
✓ La cita debe estar en estado "Completed"
✓ Verifica que el paciente tenga datos de facturación
✓ Confirma que hay configuración de tipos de factura
✓ Ve a Contabilidad → Configuración → Tipos de Factura
```

---

## 📞 Información de Soporte

**Autor:** Ronald-Ribentek  
**Versión Actual:** 17.0.1.0.0  
**Licencia:** LGPL-3 (GNU Lesser General Public License)  
**Odoo Compatible:** 17.0+  
**Estado:** Production Ready

---

## 📚 Archivos Clave

### Modelos
- [models/appointment.py](models/appointment.py) - Extensión del modelo de citas
- [models/appointment_wizard.py](models/appointment_wizard.py) - Wizard de reprogramación

### Vistas
- [views/appointment_view.xml](views/appointment_view.xml) - Todas las vistas de citas
- [views/appointment_reprogramar_wizard_view.xml](views/appointment_reprogramar_wizard_view.xml) - Vista del wizard

### Seguridad
- [security/ir.model.access.csv](security/ir.model.access.csv) - Control de acceso por rol

### Estilos
- [static/src/css/oehealth_calendar_colors.css](static/src/css/oehealth_calendar_colors.css) - Estilos personalizados

---

## 🔗 Enlaces Relacionados

- **Documentación de Odoo:** https://www.odoo.com/documentation/17.0
- **OeHealth Documentación:** https://oehealth.in
- **Comunidad Odoo:** https://github.com/OCA

---

## 📋 Changelog

### **v17.0.1.0.0** (Versión Inicial - Enero 2026)
- ✅ Sistema de estados mejorado (Scheduled, Completed, Reprogramada, Sin Asistir, Invoiced)
- ✅ Wizard de reprogramación automática
- ✅ Reportes analíticos (Asistencia y Demanda)
- ✅ Filtros temporales avanzados
- ✅ Vistas múltiples (Form, Tree, Calendar, Graph)
- ✅ Sistema de colores personalizado
- ✅ Control de acceso por roles
- ✅ Integración con facturación

---

## ✅ Checklist de Instalación

- [ ] Copiar carpeta `module_patients_citas` a `odoo17/addons/module_for_oehealth/`
- [ ] Verificar que `oehealth` esté instalado
- [ ] Verificar que `module_roles_oehealth` esté instalado
- [ ] Actualizar lista de aplicaciones en Odoo
- [ ] Instalar módulo desde Aplicaciones
- [ ] Verificar permisos en Seguridad
- [ ] Crear una cita de prueba
- [ ] Probar todos los botones de acciones
- [ ] Verificar colores en vista calendario
- [ ] Revisar reportes
- [ ] Probar wizard de reprogramación

---

## 🎓 Aprendizaje y Mejora Continua

### Para Desarrolladores
```
├── Entender flujo de estados
├── Familiarizarse con modelos OeHealth
├── Aprender sobre wizards en Odoo
├── Practicar con vistas XML
└── Estudiar seguridad en Odoo (ir.model.access.csv)
```

### Para Usuarios
```
├── Practicar creación de citas
├── Usar filtros para búsqueda rápida
├── Interpretar reportes
├── Entender estados de cita
└── Dominar wizard de reprogramación
```

---

**Última actualización:** Enero 12, 2026  
**Versión del documento:** 1.0

