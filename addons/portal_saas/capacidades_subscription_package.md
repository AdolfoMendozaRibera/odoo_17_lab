# Capacidades del Módulo `subscription_package`
> Cybrosys Technologies · Odoo 17 Community · v17.0.4.0.0

---

## Modelos que incluye

- **`subscription.package`** — Suscripción principal por cliente
- **`subscription.package.plan`** — Planes de suscripción configurables
- **`subscription.package.stage`** — Etapas del flujo Kanban
- **`subscription.package.stop`** — Razones de cierre
- **`subscription.package.product.line`** — Líneas de producto dentro de una suscripción
- **`recurrence.period`** — Períodos de recurrencia personalizados
- **`subscription.close`** — Wizard de cierre con motivo

---

## Gestión de Planes

- Crear planes con nombre, código corto y términos y condiciones
- Configurar el **período de facturación**: días, semanas, meses o años
- Elegir el **número de ocurrencias**:
  - `Ones` — dura exactamente un período y se cierra solo
  - `Until Closed Manually` — se renueva indefinidamente hasta intervención manual
  - `Custom` — se renueva N veces y luego se cierra automáticamente
- Elegir el **modo de creación de facturas**:
  - `Manually` — el admin crea la factura a mano
  - `Draft` — el cron crea la factura en borrador automáticamente
- Asignar diario contable y empresa por plan
- Ver cuántos **productos** y cuántas **suscripciones activas** usa cada plan

---

## Gestión de Suscripciones

- Crear suscripciones manualmente o automáticamente desde una orden de venta
- Asignar cliente, vendedor, plan, cuenta analítica y etiquetas
- Generar un **código de referencia único** con secuencia automática (prefijo `SUB`)
- Agregar **líneas de producto** con cantidad, precio, descuento e impuestos
- Ver el **subtotal, impuestos y total recurrente** calculados automáticamente
- Visualizar la suscripción en vista **Kanban y lista**
- Seguimiento de cambios mediante **chatter** (mensajes y actividades)

---

## Control de Fechas

- `date_started` — fecha real de inicio (inmutable, se guarda una sola vez)
- `start_date` — inicio del período de facturación actual (avanza cada ciclo)
- `next_invoice_date` — próxima fecha de cobro (calculada automáticamente)
- `close_date` — fecha estimada de vencimiento según el plan

---

## Flujo de Etapas (Kanban)

| Etapa | Categoría | Descripción |
|---|---|---|
| Draft | `draft` | Suscripción creada, pendiente de activar |
| In Progress | `progress` | Suscripción activa y facturando |
| Paused | `paused` | Suspendida temporalmente |
| Closed | `closed` | Cerrada definitivamente |

- Todas las etapas son visibles en el Kanban aunque estén vacías
- Se puede agregar etapas personalizadas desde la vista de configuración

---

## Ciclo de Vida y Acciones

- **Activar** suscripción con el botón `Start` → pasa de Draft a In Progress
- **Pausar** con el botón `Pause` → pasa a Paused
- **Reanudar** con el botón `Resume` → vuelve a In Progress
- **Cerrar** con el wizard de cierre → selecciona motivo, fecha y responsable
- **Renovar** con el botón `Renew` → crea una nueva orden de venta vinculada

---

## Facturación Automática (Cron diario)

- El proceso `close_limit_cron` se ejecuta **todos los días**
- Si `hoy == next_invoice_date` y el modo es `Draft`:
  - Crea automáticamente una factura `account.move` en estado borrador
  - Vincula la factura a la suscripción con el campo `subscription_id`
  - Avanza el `start_date` al siguiente período
- Permite **múltiples facturas** por suscripción a lo largo del tiempo
- Si `hoy == close_date` y el plan no es `Until Closed Manually`:
  - Cierra la suscripción automáticamente con motivo "Renewal Limit Exceeded"

---

## Correo de Alerta de Renovación

- Envía automáticamente un email al cliente cuando se acerca el vencimiento
- La fecha de alerta se calcula como: `vencimiento - (duración_total / 10)`
- Plantilla personalizable con nombre del cliente, nombre del plan y fecha de cierre
- Marca la suscripción con `is_to_renew = True` al enviar el aviso

---

## Integración con Órdenes de Venta

- Al confirmar una orden de venta con un producto marcado como `Is Subscription`:
  - Se crea automáticamente una `subscription.package` en estado Draft
  - Se copian las líneas de producto desde la orden
  - Se asigna el plan configurado en el producto
- La orden de venta muestra un contador de suscripciones vinculadas
- Se puede abrir la suscripción directamente desde la orden con un botón

---

## Integración con Productos

- Campo `Is Subscription` (booleano) en `product.template`
- Campo `Subscription Plan` para asignar el plan directamente en el producto
- Filtro en la ficha del producto para ver solo productos de suscripción
- Desde el plan se puede ver cuántos productos lo usan

---

## Integración con Clientes (res.partner)

- Campo `Active Subscription` (booleano) en el cliente — se activa al crear su primera suscripción
- Vista de las líneas de producto de suscripción directamente en la ficha del cliente

---

## Integración con Facturas (account.move)

- Campo `Is Subscription` en la factura
- Campo `Subscription Id` para vincular cada factura a su suscripción
- El contador `invoice_count` en la suscripción muestra todas las facturas históricas
- Botón para abrir las facturas directamente desde la suscripción

---

## Informes

- Reporte imprimible de la suscripción (subscription report view incluido en el manifest)

---

## Seguridad y Accesos

- Grupos de acceso propios del módulo (`subscription_package_groups.xml`)
- Reglas de acceso por modelo en `ir.model.access.csv`

---

## Datos de Configuración Precargados

| Dato | Descripción |
|---|---|
| Etapas | Draft, In Progress, Paused, Closed |
| Motivo de cierre | "Renewal Limit Exceeded" |
| Unidades de medida | Months, Years (categoría Time) |
| Secuencia | `SUB0001`, `SUB0002`... |
| Plantilla de correo | "Subscription: Email Renew Alert" |
| Cron job | "Check Close Limit" (diario) |

---

## Lo que el módulo NO hace

> Incluido para tener claridad total al planear extensiones.

- ❌ No controla acceso de `res.users` (no bloquea login al vencer)
- ❌ No tiene líneas de suscripción por usuario individual
- ❌ No tiene campos de "meses comprados" ni "cantidad de usuarios" en la orden
- ❌ No tiene flujo de addon para agregar usuarios a mitad del período
- ❌ No tiene período de gracia antes del cierre
- ❌ No tiene avisos escalonados (30/15/7/1 día)
- ❌ No se integra con instancias Docker ni infraestructura externa
- ❌ No tiene portal de cliente para autogestión de la suscripción
- ❌ No tiene widget configurador de meses y usuarios en la tienda

---

*Módulo base: `subscription_package` by Cybrosys Technologies · AGPL-3*