from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AppLauncherTile(models.Model):
    _name = "app.launcher.tile"
    _description = "App Launcher Tile"
    _order = "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)
    icon = fields.Binary(string="Icona", attachment=True)
    icon_filename = fields.Char()
    menu_id = fields.Many2one("ir.ui.menu", string="Menu di destinazione", ondelete="restrict")
    color_class = fields.Char(string="CSS class", help="Esempio: o_launcher_blue")
    icon_class = fields.Char(
        string="Icona (FontAwesome)",
        help="Esempio: fa-shopping-cart, fa-archive, fa-address-book"
    )
    accent_class = fields.Char(
        string="Accento (CSS)",
        help="Esempio: o_launch_accent_blue / green / orange / purple / pink"
    )

    def _find_menu_action(self, menu):
        """Ritorna la prima action trovata su menu o sui suoi discendenti."""
        menu = menu.sudo()
        if menu.action:
            return menu.action.sudo()
        for child in menu.child_id.sorted(lambda m: (m.sequence, m.id)):
            act = self._find_menu_action(child)
            if act:
                return act
        return False

    def action_open(self):
        self.ensure_one()
        if not self.menu_id:
            raise UserError(_("Nessun menu di destinazione configurato per questa tile."))
        action = self._find_menu_action(self.menu_id)
        if not action:
            raise UserError(_("Nessuna azione trovata per il menu selezionato o i suoi sottomenu."))
        return action.read()[0]
