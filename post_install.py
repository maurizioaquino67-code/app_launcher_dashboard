import base64
import os
from odoo import api, SUPERUSER_ID


def load_icon(filename):
    """Legge un'icona dalla cartella static/img e la ritorna in base64."""
    icon_path = os.path.join(
        os.path.dirname(__file__),
        "static", "img", filename
    )
    if os.path.exists(icon_path):
        with open(icon_path, "rb") as f:
            return base64.b64encode(f.read())
    return False


def post_init_hook(env):
    """
    Eseguito automaticamente dopo l'installazione del modulo.
    - Carica le icone PNG nelle tile
    - Crea il record singleton launcher.settings con i colori di default
    """

    # 1. Crea il singleton impostazioni se non esiste
    Settings = env["launcher.settings"]
    if not Settings.sudo().search([], limit=1):
        Settings.sudo().create({
            "background_color": "#1565C0",
            "label_color":      "#FFFFFF",
            "label_font_size":  15,
            "icon_bg_color":    "#1565C0",
        })

    # 2. Carica le icone nelle tile (cercandole per xmlid)
    icons = {
        "app_launcher_dashboard.tile_crm":       "crm.png",
        "app_launcher_dashboard.tile_sales":     "vendite.png",
        "app_launcher_dashboard.tile_inventory": "magazzino.png",
        "app_launcher_dashboard.tile_contacts":  "contatti.png",
    }

    for xmlid, filename in icons.items():
        tile = env.ref(xmlid, raise_if_not_found=False)
        if tile:
            icon_data = load_icon(filename)
            if icon_data:
                tile.sudo().write({
                    "icon":          icon_data,
                    "icon_filename": filename,
                })
