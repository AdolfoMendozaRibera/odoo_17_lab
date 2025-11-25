{
    "name": "User Task Manager",
    "version": "1.1.0",
    "category": "Productivity",
    "summary": "Módulo para gestionar tareas personales",
    "description": """
        Gestor de Tareas Personales
        ============================
        * Gestión de tareas por usuario
        * Estados y prioridades
        * Alertas de vencimiento
        * Filtros inteligentes
    """,
    "author": "Adolfo",
    "website": "https://yourwebsite.com",
    "license": "LGPL-3",
    "depends": ["base"],
    "data": [
        "security/task_security.xml",
        "security/ir.model.access.csv",
        "views/task_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "user_task_manager/static/src/css/task_kanban.css",
        ],
    },
    "installable": True,
    "application": True,
    "auto_install": False,
}