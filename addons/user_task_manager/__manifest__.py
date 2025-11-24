{
    "name": "User Task Manager",
    "version": "1.0",
    "category": "Productivity",
    "summary": "Modulo para gestionar tareas asignadas por usuario",
    "description": """
        Gestor de tareas asignadas por usuario.
    """,
    "author": "BlueHat",
    "website": "https://yourwebsite.com",
    "depends": ["base"],
    "data": [
        "security/task_security.xml",
        "security/ir.model.access.csv",
        "views/task_views.xml",
    ],
    "installable": True,
    "application": True,
    "assets": {
        "web.assets_backend": [
            "user_task_manager/static/src/css/task_kanban.css",
        ],
    },
}