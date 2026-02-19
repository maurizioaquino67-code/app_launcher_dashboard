from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AppLauncherTile(models.Model):
    _name = "app.launcher.tile"
    _description = "App Launcher Tile"
    _order = "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)

    # icona caricabile (png/svg) come allegato
    icon = fields.Binary(string="Icona", attachment=True)
    icon_filename = fields.Char()
    
    # tile che punta a un menu esistente di Odoo
    menu_id = fields.Many2one("ir.ui.menu", string="Menu di destinazione", ondelete="restrict")

    # opzionale: colore / css class (se vuoi)
    color_class = fields.Char(string="CSS class", help="Esempio: o_launcher_blue")
    
    icon_class = fields.Char(
        string="Icona (FontAwesome)",
        help="Esempio: fa-shopping-cart, fa-warehouse, fa-address-book"
    )
	
    accent_class = fields.Char(
        string="Accento (CSS)",
        help="Esempio: o_launch_accent_blue / green / orange / purple"
    )
    
    def _action_is_openable(self, action):
        """Prova a capire se l'azione è realmente apribile dall'utente."""
        action = action.sudo()
        if action._name == "ir.actions.act_window" and action.res_model:
            try:
                self.env[action.res_model].check_access_rights("read")
            except Exception:
                return False
        return True
        
    def _find_first_openable_action(self, menu):
        """Trova la prima action apribile scendendo nel tree dei menu."""
        menu = menu.sudo()

        if menu.action:
            act = menu.action.sudo()
            if self._action_is_openable(act):
                return act

        for child in menu.child_id.sorted(lambda m: (m.sequence, m.id)):
            act = self._find_first_openable_action(child)
            if act:
                return act
        return False
    
    def _find_menu_action(self, menu):
        """Ritorna la prima action trovata su menu o sui suoi discendenti."""
        menu = menu.sudo()
        
        if menu.action:
            return menu.action.sudo()
        
        children = menu.child_id.sorted(lambda m: (m.sequence, m.id))
        for child in children:
            act = self._find_menu_action(child)
            if act:
                return act
        return False

    def action_open(self):
        self.ensure_one()
        if not self.menu_id:
            raise UserError(_("Nessun menu di destinazione configurato per questa tile."))

        # Cerca l'azione sul menu selezionato o, se assente,
        # scende ricorsivamente nei menu figli fino a trovarne una
        action = self._find_menu_action(self.menu_id)
        if not action:
            raise UserError(_("Nessuna azione trovata per il menu selezionato o i suoi sottomenu."))

        return action.read()[0]
