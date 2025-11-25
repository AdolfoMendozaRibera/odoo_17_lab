from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
from datetime import timedelta


class UserTask(models.Model):
    _name = "user.task"
    _description = "User Task"
    _order = "priority desc, deadline asc"

    name = fields.Char(string="Título", required=True)
    description = fields.Text(string="Descripción")
    priority = fields.Selection(
        [("0", "Baja"), ("1", "Media"), ("2", "Alta")],
        string="Prioridad",
        default="1",
    )
    state = fields.Selection(
        [
            ("draft", "Borrador"),
            ("in_progress", "En Progreso"),
            ("done", "Completada"),
            ("cancelled", "Cancelada"),
        ],
        string="Estado",
        default="draft",
    )
    deadline = fields.Date(string="Fecha Límite")
    is_done = fields.Boolean(
        string="Completada",
        compute="_compute_is_done",
        store=True,
        help="Indica si la tarea está completada",
    )
    is_overdue = fields.Boolean(
        string="Vencida", compute="_compute_is_overdue", store=False
    )
    days_remaining = fields.Integer(
        string="Días Restantes", compute="_compute_days_remaining", store=False
    )
    user_id = fields.Many2one(
        "res.users",
        string="Asignado a",
        default=lambda self: self.env.user,
        required=True,
    )
    completed_date = fields.Datetime(
        string="Fecha de Completado", readonly=True, copy=False
    )
    notes = fields.Html(string="Notas Adicionales")
    active = fields.Boolean(default=True, help="Permite archivar tareas")

    # Campos calculados para estadísticas
    duration_days = fields.Integer(
        string="Días desde creación", compute="_compute_duration", store=False
    )

    @api.depends("state")
    def _compute_is_done(self):
        """Calcula si la tarea está completada"""
        for record in self:
            record.is_done = record.state == "done"

    @api.depends("deadline", "state")
    def _compute_is_overdue(self):
        """Calcula si la tarea está vencida"""
        today = fields.Date.today()
        for record in self:
            if record.deadline and record.state not in ["done", "cancelled"]:
                record.is_overdue = record.deadline < today
            else:
                record.is_overdue = False

    @api.depends("deadline")
    def _compute_days_remaining(self):
        """Calcula días restantes hasta la fecha límite"""
        today = fields.Date.today()
        for record in self:
            if record.deadline:
                delta = record.deadline - today
                record.days_remaining = delta.days
            else:
                record.days_remaining = 0

    @api.depends("create_date")
    def _compute_duration(self):
        """Calcula días desde la creación"""
        for record in self:
            if record.create_date:
                delta = fields.Datetime.now() - record.create_date
                record.duration_days = delta.days
            else:
                record.duration_days = 0

    @api.constrains("deadline")
    def _check_deadline(self):
        """Valida que si hay fecha límite, sea razonable"""
        for task in self:
            if task.deadline:
                # Advertencia si la fecha es muy antigua (más de 1 año atrás)
                one_year_ago = fields.Date.today() - timedelta(days=365)
                if task.deadline < one_year_ago:
                    raise ValidationError(
                        "La fecha límite no puede ser anterior a un año desde hoy. "
                        "Si es una tarea histórica, créala directamente en estado 'Completada'."
                    )

    def action_start(self):
        """Botón: Iniciar tarea"""
        for record in self:
            if record.state == "draft":
                record.state = "in_progress"
            else:
                raise UserError("Solo puedes iniciar tareas en estado Borrador.")

    def action_complete(self):
        """Botón: Marcar como completada"""
        for record in self:
            if record.state in ["draft", "in_progress"]:
                record.write(
                    {"state": "done", "completed_date": fields.Datetime.now()}
                )
            else:
                raise UserError(
                    "Solo puedes completar tareas en Borrador o En Progreso."
                )

    def action_reopen(self):
        """Botón: Reabrir tarea completada"""
        for record in self:
            if record.state == "done":
                record.write({"state": "in_progress", "completed_date": False})
            else:
                raise UserError("Solo puedes reabrir tareas completadas.")

    def action_cancel(self):
        """Botón: Cancelar tarea"""
        for record in self:
            if record.state not in ["done", "cancelled"]:
                record.state = "cancelled"
            else:
                raise UserError("No puedes cancelar una tarea completada o ya cancelada.")

    def action_reset_to_draft(self):
        """Botón: Volver a borrador"""
        for record in self:
            record.write({"state": "draft", "completed_date": False})

    @api.model
    def _cron_notify_overdue_tasks(self):
        """Cron: Notifica tareas vencidas (opcional, requiere mail)"""
        overdue_tasks = self.search(
            [
                ("deadline", "<", fields.Date.today()),
                ("state", "in", ["draft", "in_progress"]),
                ("active", "=", True),
            ]
        )

        # Agrupar por usuario
        users_tasks = {}
        for task in overdue_tasks:
            if task.user_id not in users_tasks:
                users_tasks[task.user_id] = []
            users_tasks[task.user_id].append(task)

        # Aquí podrías enviar notificaciones por usuario
        # Por ejemplo, usando el sistema de mensajería de Odoo
        for user, tasks in users_tasks.items():
            # Crear actividad o mensaje
            pass  # Implementar según necesidad

    @api.model
    def create(self, vals):
        """Override para logging o validaciones adicionales"""
        task = super(UserTask, self).create(vals)
        # Si se crea directamente como 'done', establecer fecha de completado
        if task.state == "done" and not task.completed_date:
            task.completed_date = fields.Datetime.now()
        return task

    def write(self, vals):
        """Override para actualizar completed_date automáticamente"""
        # Si se marca como completada, guardar fecha
        if vals.get("state") == "done" and "completed_date" not in vals:
            vals["completed_date"] = fields.Datetime.now()
        # Si se desmarca como completada, limpiar fecha
        elif vals.get("state") in ["draft", "in_progress", "cancelled"]:
            vals["completed_date"] = False

        return super(UserTask, self).write(vals)