from odoo import models, fields, api

# Mappa taglia → pixel
ICON_SIZE_MAP = {
    'xs': 65,
    's':  85,
    'm':  105,
    'l':  120,
    'xl': 130,
}

class LauncherSettings(models.Model):
    _name = "launcher.settings"
    _description = "Impostazioni Launcher"

    background_color = fields.Char(
        string="Colore sfondo dashboard",
        default="#1565C0",
    )
    label_color = fields.Char(
        string="Colore testo etichette",
        default="#FFFFFF",
    )
    label_font_size = fields.Integer(
        string="Dimensione font etichette (px)",
        default=15,
    )
    icon_bg_color = fields.Char(
        string="Colore sfondo icone",
        default="#1565C0",
    )
    icon_size = fields.Selection(
        selection=[
            ('xs', 'XS — Extra Small'),
            ('s',  'S  — Small'),
            ('m',  'M  — Medium'),
            ('l',  'L  — Large'),
            ('xl', 'XL — Extra Large'),
        ],
        string="Dimensione icone",
        default='xl',
        required=True,
    )

    @api.model
    def get_instance(self):
        """Ritorna il record singleton, creandolo se non esiste."""
        record = self.sudo().search([], limit=1, order="id asc")
        if not record:
            record = self.sudo().create({
                "background_color": "#1565C0",
                "label_color":      "#FFFFFF",
                "label_font_size":  15,
                "icon_bg_color":    "#1565C0",
                "icon_size":        "xl",
            })
        return record

    @api.model
    def get_settings(self):
        """Chiamata RPC dal JS — ritorna tutte le impostazioni grafiche."""
        r = self.get_instance()
        size_key = r.icon_size or 'xl'
        icon_px = ICON_SIZE_MAP.get(size_key, 130)
        return {
            "background_color": r.background_color or "#1565C0",
            "label_color":      r.label_color or "#FFFFFF",
            "label_font_size":  r.label_font_size or 15,
            "icon_bg_color":    r.icon_bg_color or "#1565C0",
            "icon_size":        size_key,
            "icon_px":          icon_px,
        }

    @api.model
    def action_open_settings(self):
        """Apre sempre il form del record singleton."""
        record = self.get_instance()
        return {
            "type": "ir.actions.act_window",
            "name": "Impostazioni Launcher",
            "res_model": "launcher.settings",
            "view_mode": "form",
            "res_id": record.id,
            "target": "current",
        }
