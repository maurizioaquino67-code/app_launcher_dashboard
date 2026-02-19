from odoo import models, fields, api

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
        default="#FFFFFF",
    )

    @api.model
    def get_instance(self):
        """Ritorna il record singleton, creandolo se non esiste."""
        record = self.sudo().search([], limit=1, order="id asc")
        if not record:
            record = self.sudo().create({
                "background_color": "#1565C0",
                "label_color": "#FFFFFF",
                "label_font_size": 15,
                "icon_bg_color": "#FFFFFF",
            })
        return record

    @api.model
    def get_settings(self):
        """Chiamata RPC dal JS — ritorna tutte le impostazioni grafiche."""
        r = self.get_instance()
        return {
            "background_color": r.background_color or "#1565C0",
            "label_color": r.label_color or "#FFFFFF",
            "label_font_size": r.label_font_size or 15,
            "icon_bg_color": r.icon_bg_color or "#FFFFFF",
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
