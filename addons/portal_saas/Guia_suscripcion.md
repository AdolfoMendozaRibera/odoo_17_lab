# Guía del Módulo de Suscripción Dinámica — Odoo 17

> **Proyecto:** micro_SaaS + Suscripción por Usuario / Período Dinámico
> **Plataforma:** Odoo 17 · Docker · Community
> **Descripción:** Flujo completo — Compra · Instancia · Usuarios · Renovación · Vencimiento

---

## Tabla de Contenidos

- [Sección 0 — Modelos de datos](#sección-0--modelos-de-datos)
- [Sección 1 — Compra inicial](#sección-1--compra-inicial)
- [Sección 2 — Asignación de instancias](#sección-2--asignación-de-instancias)
- [Sección 3 — Gestión de usuarios](#sección-3--gestión-de-usuarios)
- [Sección 4 — Agregar un nuevo usuario (Addon)](#sección-4--agregar-un-nuevo-usuario-addon)
- [Sección 5 — Control de vencimiento y suspensión](#sección-5--control-de-vencimiento-y-suspensión)
- [Sección 6 — Flujo de renovación](#sección-6--flujo-de-renovación)
- [Sección 7 — Estados de la suscripción](#sección-7--estados-de-la-suscripción)
- [Sección 8 — Módulos a desarrollar](#sección-8--módulos-a-desarrollar)

---

## Sección 0 — Modelos de datos

> **Los "cajones" del sistema — La base de datos: qué guardamos y por qué**

Antes de entender el flujo, hay que entender **dónde vive cada dato**. En Odoo, los "modelos" son como las tablas de una base de datos: cada uno guarda un tipo específico de información. Vamos a necesitar 6 modelos principales.

---

### 🗂️ Plan de Suscripción — `subscription.plan`

Es el **catálogo de precios**. Aquí defines que un usuario cuesta, por ejemplo, 100 Bs al mes. Si en el futuro cambias el precio, solo cambias el plan. No afecta a los clientes que ya tienen suscripción activa porque sus facturas ya fueron generadas.

| Campo | Tipo | Descripción |
|---|---|---|
| `nombre` | Texto | Nombre del plan (ej: "Plan Estándar") |
| `precio_por_usuario_mes` | Decimal | Costo por usuario por mes (ej: 100 Bs) |
| `moneda` | Referencia | Moneda del precio |
| `activo` | Sí/No | Si el plan está disponible para vender |

---

### 📄 Suscripción Principal — `subscription.subscription`

Es el **registro central de cada cliente**. Piénsalo como el contrato firmado: dice quién es el cliente, qué plan tiene, en qué instancia está y en qué estado se encuentra. Cada empresa cliente tiene exactamente **una suscripción**.

| Campo | Tipo | Descripción |
|---|---|---|
| `empresa_cliente` | Referencia | El cliente (res.partner) |
| `instancia` | Referencia | La instancia Odoo asignada |
| `plan` | Referencia | El plan contratado |
| `estado` | Selección | borrador / activa / pausada / cancelada |
| `orden_venta` | Referencia | La orden que originó la suscripción |

---

### 👤 Línea por Usuario — `subscription.line` ← La pieza más importante

Este es el **corazón del sistema**. En lugar de decir "esta empresa tiene 5 usuarios hasta el mes 7", el sistema dice **"este usuario específico está pagado desde el día X hasta el día Y"**. Esto permite que cada empleado tenga su propia fecha de vencimiento independiente, lo cual resuelve exactamente el problema de agregar usuarios a mitad del período.

| Campo | Tipo | Descripción |
|---|---|---|
| `suscripcion` | Referencia | Suscripción principal a la que pertenece |
| `usuario` | Referencia | El usuario de Odoo (res.users) |
| `meses_pagados` | Entero | Cuántos meses se pagaron para este usuario |
| `fecha_inicio` | Fecha | Cuándo empieza el período pagado |
| `fecha_fin` | Fecha (calculada) | fecha_inicio + meses_pagados |
| `factura` | Referencia | La factura que originó esta línea |
| `estado` | Selección | activa / expirada / inactiva_usuario |

> 💡 **¿Por qué una línea por usuario y no una por empresa?**
>
> Imagina que la empresa ABC tiene 5 empleados pagados por 7 meses y al mes 4 entra un empleado nuevo. Si usáramos un solo registro para toda la empresa, sería muy difícil saber cuándo vence el nuevo. Con **una línea por usuario**, el nuevo simplemente tiene su propia línea con fechas independientes. Sin líos, sin prorrateos complicados.

---

### 🏗️ Instancia Odoo — `saas.instance`

Cada instancia es **una instalación de Odoo** con su propia base de datos y su propia URL (ej: *empresa.tuapp.com*). Una instancia puede alojar a varias empresas clientes al mismo tiempo. Este modelo registra cuántos usuarios puede tener como máximo y cuántos tiene actualmente.

| Campo | Tipo | Descripción |
|---|---|---|
| `nombre_base_datos` | Texto | Nombre de la DB (ej: "empresa_abc") |
| `empresas_cliente` | Muchos (many2many) | Las empresas que usan esta instancia |
| `url_acceso` | Texto | La URL del Odoo del cliente |
| `estado` | Selección | creando / activa / detenida |
| `max_usuarios` | Entero | Límite máximo de usuarios |
| `usuarios_activos` | Entero (calculado) | Suma de líneas activas en esta instancia |

---

### 🧾 Factura — `account.move`

Es el modelo estándar de Odoo para facturas, pero le agregamos un campo que la vincula a la suscripción. Se genera **una factura por cada evento de cobro**: la compra inicial, agregar un usuario nuevo, renovar, etc.

| Campo | Tipo | Descripción |
|---|---|---|
| `suscripcion` | Referencia (campo nuevo) | Vincula la factura a su suscripción |
| `tipo` | Selección | Siempre "factura de cliente" |
| `estado_pago` | Selección | pagada / pendiente |
| `lineas` | One2many | N usuarios × precio por mes |

---

### 🛒 Orden de Venta — `sale.order`

Es el modelo estándar de Odoo, al que le agregamos tres campos clave. Es el punto de partida de todo: sin orden de venta no hay factura, sin factura no hay suscripción.

| Campo | Tipo | Descripción |
|---|---|---|
| `suscripcion` | Referencia (campo nuevo) | Vincula la orden a su suscripción |
| `meses` | Entero (campo nuevo) | Cuántos meses compra el cliente |
| `cantidad_usuarios` | Entero | Cuántos usuarios se están comprando |
| `tipo_orden` | Selección | nueva / addon / renovacion |

---

### 📐 Fórmula de cobro

```
Total = precio_plan × cantidad_usuarios × meses_elegidos

Ejemplo: 100 Bs × 5 usuarios × 7 meses = 3,500 Bs
         (se cobra todo por adelantado en una sola factura)
```

---

## Sección 1 — Compra Inicial

> **Del primer clic del cliente hasta que su Odoo está listo**

Este es el flujo que recorre un cliente nuevo. Son **7 pasos** que mezclan acciones del cliente, del sistema y del administrador.

### Pasos del flujo

**1. El cliente entra a la tienda del portal**
Ve un único producto llamado "Suscripción Odoo". Solo puede agregar uno al carrito (el sistema lo valida). No hay opciones confusas de mensual/semestral/anual: eso se elige en el siguiente paso.

**2. Configura su suscripción con el widget dinámico**
En la ficha del producto aparece un configurador interactivo: un selector de meses (de 1 a 36) y un campo para escribir cuántos usuarios necesita. El precio total se actualiza automáticamente en tiempo real.
*Ej: mueve el selector a 7 meses, escribe 5 usuarios → se muestra "Total: 3,500 Bs".*

**3. Agrega al carrito y paga**
El sistema guarda en la orden de venta los meses y usuarios elegidos (no solo el precio). El cliente paga por transferencia, QR u otro método disponible.

**4. La orden llega al Odoo Maestro**
El administrador recibe la orden de venta en su panel. Puede ver el cliente, los meses comprados y la cantidad de usuarios. La orden llega en estado "borrador".

**5. El admin verifica el pago**
Una vez que confirma que el dinero llegó, confirma la orden. Esto activa la generación automática de la factura.

**6. Se genera la factura automáticamente**
Al confirmar la orden, el sistema crea la factura y la marca como pagada. La factura dice exactamente: N usuarios × X meses × 100 Bs = Total.

**7. Se crean la suscripción y las líneas por usuario**
Cuando la factura queda como pagada, se dispara una acción automática que crea la suscripción principal y una línea de suscripción por cada usuario comprado, con fecha de inicio hoy y fecha de fin en X meses.

### Flujo resumido

```
Tienda → Configurador → Carrito → Pago → Odoo Maestro → Factura pagada → Suscripción + Líneas
```

> ⚙️ **¿Qué es la "acción automática"?**
>
> En Odoo existe la posibilidad de configurar reglas que digan "cuando pase X, hacer Y automáticamente". En este caso, la regla dice: **cuando una factura vinculada a una suscripción cambie a estado pagada → crear suscripción + líneas de usuario**. No hace falta que el admin haga nada manualmente.

### Ejemplo

> La empresa **Boticas del Sur** elige 7 meses y 5 usuarios (total 3,500 Bs). El admin aprueba el pago. El sistema crea automáticamente la suscripción con **5 líneas de usuario**, cada una con fecha inicio hoy y fecha fin en 7 meses.

---

## Sección 2 — Asignación de Instancias

> **Dónde y cómo se aloja el Odoo del cliente (micro_SaaS)**

Una vez creada la suscripción, el módulo **micro_SaaS** se encarga de preparar el Odoo donde el cliente va a trabajar. Una **instancia** es una instalación de Odoo con su propia base de datos. Varias empresas pueden compartir la misma instancia para aprovechar mejor los recursos del servidor.

### Pasos del flujo

**1. El sistema busca una instancia con cupo disponible**
Al activarse la suscripción, el módulo revisa si existe alguna instancia donde `usuarios_activos < max_usuarios`. Si encuentra una, asigna el cliente ahí.

**2. Si no hay cupo: crear instancia nueva**
micro_SaaS crea una nueva base de datos PostgreSQL, configura el subdominio (ej: *boticasdelsur.tuapp.com*), instala los módulos base y crea el usuario administrador del cliente.

**3. Se vincula la suscripción con la instancia**
El campo `instancia` de la suscripción se llena con la instancia asignada. Así el sistema siempre sabe en qué servidor está cada cliente.

**4. Se notifica al cliente por email**
El cliente recibe un correo con su URL de acceso, usuario, contraseña temporal, fecha de vencimiento y el número de usuarios que puede crear.

### Diagrama de decisión

```
¿Existe instancia con cupo?
        │
   ┌────┴────┐
   Sí        No
   │          │
Asignar    Crear nueva
cliente    instancia
   │          │
   └────┬─────┘
        │
Vincular suscripción ← instancia
        │
  Notificar al cliente por email
```

> ⚠️ **Regla de negocio crítica:** La instancia siempre debe tener como límite máximo la **suma de líneas de suscripción activas** de todas las empresas que aloja. Si hay 2 empresas con 5 usuarios cada una, el límite máximo es 10. Intentar crear el usuario 11 debe ser bloqueado.

---

## Sección 3 — Gestión de Usuarios en Período Activo

> **Qué pasa cuando un empleado se va o llega uno nuevo**

Una vez activa la suscripción, el día a día consiste en que el admin va agregando o quitando empleados de su Odoo.

### Escenario 1 — Estado normal ✅

Todos los usuarios tienen una línea de suscripción activa y vigente. El acceso a la instancia funciona normalmente. No hay ninguna acción requerida.

### Escenario 2 — Un empleado se va ➖

El admin desactiva al usuario en su Odoo (`res.users.active = False`). Esto bloquea el acceso de esa persona inmediatamente. **Sin embargo, la línea de suscripción sigue activa hasta su fecha de vencimiento original.** ¿Por qué? Porque ese período ya fue pagado por adelantado y no hay reembolso.

### Escenario 3 — Llega un empleado nuevo ➕

El admin intenta crear un usuario nuevo. El sistema detecta que no existe una línea de suscripción activa para ese usuario y **bloquea la creación hasta que se pague el addon correspondiente**. También envía una notificación automática al administrador explicando qué debe hacer.

### Ejemplo visual — Línea de tiempo

```
Empresa ABC · 5 empleados · 7 meses · 3,500 Bs pagados

[Mes 1──────── Mes 3 ─────── Mes 5 ──── Mes 7]   ← Usuarios 1-5 pagados
[Usuarios 1-4 activos │ Emp.5 sale │ Línea sigue, sin acceso, sin reembolso]
[Bloqueado hasta pagar │ Emp.Nuevo pagado desde día 15 del mes 4]
```

> 🔑 **La regla más importante:** El sistema no rebaja el precio porque un empleado se fue. **El precio pagado es fijo para el período comprado.** Lo que sí puede hacer el cliente es renovar solo con los empleados activos cuando llegue el momento.

---

## Sección 4 — Agregar un Nuevo Usuario (Addon)

> **El flujo completo cuando entra un empleado nuevo a mitad del período**

Lo llamamos **"addon"** porque no es una suscripción nueva, sino un usuario adicional que se agrega a una suscripción ya existente.

### Pasos del flujo

**1. El admin crea el usuario en su Odoo**
El sistema detecta que no hay una línea de suscripción activa para ese usuario.

**2. El sistema genera una alerta automática**
Se envía un correo al admin con el nombre del usuario sin suscripción y un enlace directo para pagar el addon.

**3. El admin va al portal y configura el addon**
En la sección "Mi Suscripción" del portal, el admin elige cuántos meses quiere pagar para ese empleado. El precio se calcula automáticamente.

**4. Paga y el sistema activa al usuario**
Se genera una orden de tipo "addon", se crea la factura, y al confirmarse el pago se crea la línea de suscripción. El usuario queda habilitado en la instancia.

### Flujo resumido

```
Nuevo usuario creado en instancia
        ↓
Sistema detecta: sin subscription.line
        ↓
Alerta automática al admin
        ↓
Admin compra addon en portal (elige N meses)
        ↓
Factura pagada → subscription.line.create()
        ↓
res.users.active = True ← usuario habilitado
```

### Ejemplo detallado

```
Contexto: 5 usuarios pagados por 7 meses desde el mes 1.
Hoy es el día 15 del mes 4. El jefe agrega a María García.

nueva_orden = {
    tipo_orden:        "addon",
    empresa_cliente:   empresa_abc,
    suscripcion_padre: sub_abc,       # vincula con la suscripción existente
    usuario_nuevo:     maria_garcia,
    meses:             7,             # el jefe elige 7 meses
    total:             700 Bs         # 1 usuario × 7 meses × 100 Bs
}

# Al confirmar el pago:
nueva_linea = {
    usuario:      maria_garcia,
    fecha_inicio: 15/mes4,
    fecha_fin:    15/mes11,    # fecha independiente del resto del equipo
    estado:       "activa"
}

# El resto del equipo vence al final del mes 7.
# María vence el día 15 del mes 11. Fechas independientes ✓
```

> 💡 **Opción "Sincronizar con el equipo":** Si el admin activa esta opción, el sistema calcula los meses restantes hasta el vencimiento del grupo y cobra solo esos meses para el usuario nuevo. Así todos vencen el mismo día y la renovación grupal es más sencilla.

> ⚠️ **¿Qué pasa si el usuario nuevo intenta trabajar antes de pagar?** No puede. El sistema solo habilita el acceso cuando la factura del addon queda marcada como pagada.

---

## Sección 5 — Control de Vencimiento y Suspensión

> **Qué hace el sistema cada día para gestionar los plazos**

Todos los días a medianoche, el sistema ejecuta un **proceso automático** que revisa todas las líneas de suscripción y toma decisiones según las fechas de vencimiento.

### Sistema de avisos escalonados

| Tiempo antes del vencimiento | Acción |
|---|---|
| 30 días | Correo informativo tranquilo |
| 15 días | Correo con tono de urgencia |
| 7 días | Correo urgente + banner en el portal |
| 1 día | Correo de última llamada + notificación al admin del sistema |

Todos los correos incluyen un botón directo de renovación.

### Al llegar la fecha de vencimiento

**Suspensión parcial** — Solo algunos usuarios vencieron:
- Solo se bloquean los usuarios con línea vencida
- Los demás siguen trabajando normalmente
- Estado de la suscripción: `parcialmente_activa`

**Suspensión total** — Todos los usuarios vencieron:
- Se bloquea el acceso de todos (`res.users.active = False`)
- Estado: `pausada`
- La instancia sigue corriendo (datos seguros)
- Empieza el **período de gracia de 30 días**

### Proceso después del vencimiento total

**Días 1–30 (período de gracia):**
El cliente puede renovar y recuperar el acceso inmediatamente. Los datos no se tocan.

**Día 30 sin renovar:**
El sistema envía un último correo con opción de descargar backup. El admin del sistema puede archivar la instancia o dar más tiempo.

**Cancelación definitiva:**
La instancia se detiene, la suscripción pasa a estado `cancelada`. Los datos se guardan en backup por **90 días adicionales** y luego se eliminan de forma permanente.

> ⚠️ **Nunca eliminar datos sin backup previo** y sin haber notificado al cliente con suficiente antelación.

---

## Sección 6 — Flujo de Renovación

> **Cómo el cliente extiende su suscripción**

Renovar es muy parecido a comprar por primera vez, con la diferencia de que el sistema ya conoce a los usuarios y puede calcular inteligentemente las nuevas fechas.

### Pasos del flujo

**1. El admin entra al portal y va a "Mi Suscripción"**
Ve todos sus usuarios, cuáles están activos, cuáles vencieron, y las fechas exactas de cada uno.

**2. Elige qué renovar y por cuántos meses**
Puede renovar todos los usuarios a la vez o seleccionar solo algunos. Por ejemplo, si salió un empleado, puede renovar solo los 4 restantes.

**3. El sistema calcula las nuevas fechas automáticamente**
- Si renueva **antes de vencer**: nueva fecha inicio = fecha fin actual *(sin perder días)*
- Si renueva **después de vencer**: nueva fecha inicio = fecha del pago

**4. Paga y el sistema reactiva el acceso**
Orden tipo `renovacion` → factura → pago → líneas actualizadas → `res.users.active = True` → correo de confirmación.

### Flujo resumido

```
Portal "Mi Suscripción"
        ↓
Elegir usuarios + meses
        ↓
Orden tipo "renovacion"
        ↓
Factura → Pago
        ↓
Líneas de suscripción actualizadas
        ↓
res.users.active = True ← acceso restaurado ✓
```

---

## Sección 7 — Estados de la Suscripción

> **Cómo saber en qué momento está cada cliente**

Cada suscripción tiene un estado que indica en qué punto del ciclo de vida se encuentra.

### Ciclo completo de estados

```
borrador → pago_pendiente → activa → parcialmente_activa → pausada ⟳ activa (renovada) → cancelada
```

### Descripción de cada estado

| Estado | Color | Descripción |
|---|---|---|
| `borrador` | ⚫ Gris | La orden fue creada pero no se ha confirmado el pago. Sin acceso a la instancia. |
| `pago_pendiente` | 🟡 Amarillo | Orden confirmada y factura generada. Esperando recibir el pago. |
| `activa` | 🟢 Verde | Todos los usuarios tienen líneas vigentes. Estado normal de operación. |
| `parcialmente_activa` | 🟠 Naranja | Algunos usuarios vencieron y están bloqueados. Otros siguen activos. |
| `pausada` | 🔴 Rojo | Todos los usuarios bloqueados. Período de gracia de 30 días activo. |
| `cancelada` | ⚫ Gris | Definitivamente terminada. Datos en backup por 90 días adicionales. |

> 🔄 **¿Puede volver de "cancelada" a "activa"?** Sí, pero requiere intervención manual del administrador: restaurar el backup y crear una nueva suscripción desde cero.

---

## Sección 8 — Módulos a Desarrollar

> **Qué hay que programar y en qué orden hacerlo**

Todo el sistema se implementa en **tres módulos de Odoo**. Uno ya existe (micro_SaaS) y solo necesita ampliarse. Los otros dos son nuevos.

> **Orden recomendado:** Primero la base de datos y la lógica → luego el portal → finalmente la integración con micro_SaaS.

---

### 📦 `subscription_dynamic` — Desarrollar primero

**¿Qué hace?** Es el núcleo de todo el sistema. Define los modelos de datos y contiene toda la lógica de negocio.

**Incluye:**
- Los 6 modelos de datos descritos en la Sección 0
- El proceso diario automático que revisa vencimientos (`ir.cron`)
- Las reglas de automatización: cuando factura = pagada → crear suscripción
- Las 4 plantillas de correo para los avisos de vencimiento
- Las acciones sobre `res.users` (bloquear / desbloquear acceso)
- Integración con `account.move` y `sale.order`

**Depende de:** `sale`, `account`, `mail` *(módulos estándar de Odoo)*

---

### 🌐 `subscription_portal` — Desarrollar segundo

**¿Qué hace?** Agrega toda la experiencia del cliente en el portal web.

**Incluye:**
- Widget de JavaScript con selector de meses y usuarios (cálculo en tiempo real)
- Página "Mi Suscripción": lista de usuarios con fechas de vencimiento
- Flujo de compra de addon para nuevos empleados
- Flujo de renovación con selección de usuarios individuales
- Opción "Sincronizar con el equipo" en el configurador
- Historial completo de facturas

**Depende de:** `subscription_dynamic`, `website_sale`

---

### 🔧 `micro_saas` — Ampliar el módulo existente (tercero)

**¿Qué cambia?** El módulo existente necesita conocer el concepto de suscripción para controlar el acceso de los usuarios.

**Se agrega:**
- Campo `empresas_cliente` (Many2many) — para que una instancia aloje N empresas
- Método `verificar_cupo_usuarios()` — bloquea si se excede el límite
- Hook `al_activar_suscripcion()` — habilita o deshabilita usuarios automáticamente
- Relación con `subscription.subscription` para saber el cupo por empresa

**Importante:** Al ser una ampliación, usar **herencia de modelos de Odoo** para no romper el comportamiento actual.

---

## Reglas de Negocio — No olvidar al programar

| # | Regla | Por qué |
|---|---|---|
| ✅ 1 | Un usuario solo puede tener **1 línea activa** por suscripción | Evitar cobro doble |
| ✅ 2 | Al desactivar un usuario, su línea **no se elimina** | Ya fue cobrado, se conserva el registro |
| ✅ 3 | Todo SO de addon debe **referenciar la suscripción padre** | Trazabilidad completa |
| ✅ 4 | La instancia solo puede tener usuarios **≤ suma de líneas activas** | Control de cupo |
| ✅ 5 | Siempre debe existir un **período de gracia de 30 días** antes de cancelar | Proteger al cliente |
| ❌ 6 | **Nunca eliminar datos** sin backup previo y sin notificar al cliente | Política de retención y confianza |

---

*Documento generado para el equipo de desarrollo del proyecto micro_SaaS — Odoo 17*