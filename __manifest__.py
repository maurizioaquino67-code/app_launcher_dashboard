{
    "name": "App Launcher Dashboard",
    "version": "18.0.1.0.0",
    "category": "Tools",
    "summary": "Dashboard a icone per aprire rapidamente le sezioni di Odoo",
    "depends": ["base", "web", "sale", "stock", "contacts", "crm", "hr"],
    "data": [
        "security/ir.model.access.csv",
        "views/launcher_tile_views.xml",
        "views/launcher_settings_views.xml",
        "views/launcher_menu.xml",
        "data/launcher_tile_data.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "app_launcher_dashboard/static/src/css/launcher.css",
            "app_launcher_dashboard/static/src/js/launcher_bg.js",
        ],
    },
    "post_init_hook": "post_init_hook",
    "application": True,
    "installable": True,
    "auto_install": False,
    "license": "LGPL-3",
}
