# App Launcher Dashboard — Odoo 18

![Odoo](https://img.shields.io/badge/Odoo-18.0-875A7B?style=flat-square&logo=odoo)
![License](https://img.shields.io/badge/License-LGPL--3-blue?style=flat-square)
![Version](https://img.shields.io/badge/Version-18.0.1.1.0-green?style=flat-square)

Un modulo per Odoo 18 che aggiunge una **dashboard a icone** per accedere rapidamente alle sezioni principali dell'applicazione, con stile ispirato a Odoo Enterprise.

---

## Funzionalità

- Dashboard con tile/icone cliccabili che aprono qualsiasi menu di Odoo
- Icone personalizzabili: immagine PNG/SVG caricabile o FontAwesome come fallback
- **5 taglie icone** selezionabili dalle Impostazioni: XS / S / M / L / XL
- Colori di sfondo, icone ed etichette configurabili
- Navigazione intelligente: funziona anche con menu padre (scende automaticamente ai sottomenu figli)
- Griglia fluida che si adatta alla larghezza dello schermo
- Effetto hover "lift" sulle icone
- 5 tile preconfigurate all'installazione: CRM, Vendite, Magazzino, Contatti, Dipendenti

---

## Screenshot

> La dashboard con le tile di default dopo l'installazione:

| CRM | Vendite | Magazzino | Contatti | Dipendenti |
|-----|---------|-----------|---------|-----------|
| 🔵 Blu | 🔴 Rosso | 🟢 Verde | 🟣 Viola | 🟤 Arancione |

---

## Requisiti

| Componente | Versione |
|---|---|
| Odoo | 18.0 |
| Python | 3.10+ |
| Moduli Odoo richiesti | `base`, `web`, `sale`, `stock`, `contacts`, `crm`, `hr` |

---

## Installazione

### 1. Copia il modulo

```bash
cp -r app_launcher_dashboard /path/to/odoo/custom-addons/
```

### 2. Aggiorna la lista dei moduli

Vai su **Impostazioni → Tecnico → Aggiorna lista moduli** oppure riavvia Odoo con:

```bash
./odoo-bin -u all -d nome_database
```

### 3. Installa il modulo

Vai su **Impostazioni → App**, cerca `App Launcher Dashboard` e clicca **Installa**.

Al termine dell'installazione il modulo:
- Crea automaticamente le 5 tile di default (CRM, Vendite, Magazzino, Contatti, Dipendenti)
- Carica le icone PNG preconfigurate in stile Enterprise
- Crea il record delle impostazioni con colori e dimensioni di default

---

## Disinstallazione pulita

Se devi disinstallare completamente il modulo e pulire il database, esegui questi comandi psql **nell'ordine indicato**:

```bash
psql -U odoo -d nome_database
```

```sql
-- 1. Cancella i dati
DELETE FROM app_launcher_tile;
DELETE FROM launcher_settings;

-- 2. Cancella le tabelle
DROP TABLE IF EXISTS app_launcher_tile CASCADE;
DROP TABLE IF EXISTS launcher_settings CASCADE;

-- 3. Cancella modelli e campi
DELETE FROM ir_model_fields WHERE model IN ('app.launcher.tile', 'launcher.settings');
DELETE FROM ir_model_constraint WHERE model IN (
    SELECT id FROM ir_model WHERE model IN ('app.launcher.tile', 'launcher.settings')
);
DELETE FROM ir_model_relation WHERE model IN (
    SELECT id FROM ir_model WHERE model IN ('app.launcher.tile', 'launcher.settings')
);
DELETE FROM ir_model WHERE model IN ('app.launcher.tile', 'launcher.settings');

-- 4. Cancella permessi
DELETE FROM ir_model_access WHERE name LIKE '%launcher%';

-- 5. Cancella viste, menu e azioni
DELETE FROM ir_ui_view WHERE model IN ('app.launcher.tile', 'launcher.settings');
DELETE FROM ir_act_window WHERE res_model IN ('app.launcher.tile', 'launcher.settings');
DELETE FROM ir_act_server WHERE model_id IN (
    SELECT id FROM ir_model WHERE model IN ('app.launcher.tile', 'launcher.settings')
);
DELETE FROM ir_ui_menu WHERE id IN (
    SELECT res_id FROM ir_model_data
    WHERE module = 'app_launcher_dashboard' AND model = 'ir.ui.menu'
);

-- 6. Cancella riferimenti al modulo
DELETE FROM ir_model_data WHERE module = 'app_launcher_dashboard';
DELETE FROM ir_model_data WHERE module = 'base' AND name = 'module_app_launcher_dashboard';

-- 7. Cancella il modulo dalla lista
DELETE FROM ir_module_module WHERE name = 'app_launcher_dashboard';

-- 8. Verifica pulizia (devono restituire 0)
SELECT COUNT(*) FROM ir_model_data WHERE module = 'app_launcher_dashboard';
SELECT COUNT(*) FROM ir_module_module WHERE name = 'app_launcher_dashboard';
```

---

## Utilizzo

### Accedere alla dashboard

Dopo l'installazione trovi il menu **Launcher** nella barra di navigazione principale di Odoo:

- **Launcher → Dashboard** — mostra le tile/icone
- **Launcher → Impostazioni** — configura aspetto e dimensioni

### Aggiungere una nuova tile

1. Vai su **Launcher → Dashboard**
2. Clicca **Nuovo**
3. Compila i campi:
   - **Nome** — etichetta visualizzata sotto l'icona
   - **Sequenza** — ordine di visualizzazione (numeri più bassi = prima)
   - **Menu di destinazione** — seleziona il menu Odoo a cui punta la tile
   - **Icona** — carica un'immagine PNG/SVG (opzionale)
   - **Icona FontAwesome** — classe FA come `fa-shopping-cart` (usata se non c'è immagine)
   - **Accento CSS** — colore di sfondo del quadrato icona (vedi tabella classi sotto)
4. Salva

> **Tip:** puoi selezionare sia un menu foglia che un menu padre. Se selezioni un menu padre (es. "Vendite"), il modulo scenderà automaticamente ai sottomenu per trovare la prima azione disponibile.

### Configurare l'aspetto

Vai su **Launcher → Impostazioni** per personalizzare:

| Campo | Descrizione | Default |
|---|---|---|
| Colore sfondo dashboard | Colore di sfondo della pagina | `#1565C0` (blu) |
| Colore sfondo icone | Colore del quadrato dietro l'icona | `#1565C0` (blu) |
| Dimensione icone | Taglia XS / S / M / L / XL | `XL` |
| Colore testo | Colore delle etichette sotto le icone | `#FFFFFF` (bianco) |
| Dimensione font (px) | Dimensione del testo delle etichette | `15` |

I cambiamenti vengono applicati **dinamicamente** senza ricaricare la pagina.

### Dimensioni icone disponibili

| Taglia | Pixel | Note |
|---|---|---|
| XS | 65 px | Molto compatta, ideale per schermi piccoli |
| S | 85 px | Compatta |
| M | 105 px | Bilanciata |
| L | 120 px | Grande |
| XL | 130 px | Extra grande — default |

> Il border-radius e la dimensione delle icone FontAwesome si scalano automaticamente in proporzione alla taglia selezionata.

---

## Struttura del modulo

```
app_launcher_dashboard/
├── __init__.py
├── __manifest__.py
├── post_install.py                  # Hook post-installazione
├── models/
│   ├── __init__.py
│   ├── launcher_tile.py             # Modello app.launcher.tile
│   └── launcher_settings.py        # Modello singleton launcher.settings
├── views/
│   ├── launcher_tile_views.xml      # Vista kanban, list, form + action
│   ├── launcher_settings_views.xml  # Vista form impostazioni
│   └── launcher_menu.xml            # Definizione menu
├── data/
│   └── launcher_tile_data.xml       # 5 tile preconfigurate
├── security/
│   └── ir.model.access.csv          # Permessi di accesso
└── static/
    ├── img/
    │   ├── crm.png
    │   ├── vendite.png
    │   ├── magazzino.png
    │   ├── contatti.png
    │   └── dipendenti.png
    └── src/
        ├── css/launcher.css
        └── js/launcher_bg.js        # Applica colori e dimensioni dinamicamente
```

---

## Modelli

### `app.launcher.tile`

| Campo | Tipo | Descrizione |
|---|---|---|
| `name` | Char | Nome della tile (obbligatorio) |
| `sequence` | Integer | Ordine di visualizzazione |
| `menu_id` | Many2one | Menu Odoo di destinazione |
| `icon` | Binary | Immagine icona (PNG/SVG) |
| `icon_class` | Char | Classe FontAwesome (es. `fa-shopping-cart`) |
| `accent_class` | Char | Classe CSS colore sfondo (es. `o_launch_accent_blue`) |
| `color_class` | Char | Classe CSS aggiuntiva |

### `launcher.settings` (singleton)

| Campo | Tipo | Descrizione |
|---|---|---|
| `background_color` | Char | Colore sfondo dashboard |
| `icon_bg_color` | Char | Colore sfondo icone |
| `icon_size` | Selection | Taglia icone: `xs` / `s` / `m` / `l` / `xl` |
| `label_color` | Char | Colore testo etichette |
| `label_font_size` | Integer | Dimensione font etichette (px) |

---

## Classi CSS accent disponibili

| Classe | Colore | Tile di default |
|---|---|---|
| `o_launch_accent_blue` | Blu `#3474C1` | CRM |
| `o_launch_accent_green` | Verde `#27AE60` | Magazzino |
| `o_launch_accent_orange` | Rosso `#E74C3C` | Vendite |
| `o_launch_accent_purple` | Viola `#8E44AD` | Contatti |
| `o_launch_accent_brown` | Arancione `#D35400` | Dipendenti |
| `o_launch_accent_pink` | Rosa `#E91E8C` | — |

---

## Changelog

### v18.0.1.1.0
- ✨ Aggiunta tile **Dipendenti** con icona preconfigurata
- ✨ Aggiunto controllo **dimensione icone** (XS / S / M / L / XL) nelle Impostazioni
- ✨ Dimensione applicata dinamicamente via JS con border-radius e font proporzionali
- ✨ Aggiunta classe CSS `o_launch_accent_brown`
- ✨ Aggiunta dipendenza modulo `hr`
- 🔧 Rimosso metodo inutilizzato `_find_first_openable_action`
- 🔧 Allineamento default `icon_bg_color` tra modello e post_install
- 🔧 Rimosso import inutilizzato `SUPERUSER_ID` da post_install

### v18.0.1.0.0
- 🎉 Release iniziale
- Dashboard kanban con tile/icone in stile Odoo Enterprise
- 4 tile di default: CRM, Vendite, Magazzino, Contatti
- Impostazioni colori (sfondo, icone, etichette, font)
- Post-install hook per caricamento automatico icone e impostazioni
- Servizio JS per applicazione dinamica dei colori

---

## Licenza

Questo modulo è distribuito sotto licenza **LGPL-3**.
Vedi il file [LICENSE](LICENSE) per i dettagli completi.

---

## Autore

Sviluppato con ❤️ per Odoo 18.

Contributi, segnalazioni di bug e pull request sono benvenuti!

---

## Contributing

Contributi, segnalazioni di bug e suggerimenti sono benvenuti! Ecco come partecipare:

### Come contribuire

1. **Fai il Fork** del repository cliccando **Fork** in alto a destra su GitHub
2. **Clona** il tuo fork localmente:
   ```bash
   git clone https://github.com/tuo-username/app_launcher_dashboard.git
   cd app_launcher_dashboard
   ```
3. **Crea un branch** per la tua modifica:
   ```bash
   git checkout -b feat/nome-della-funzionalita
   ```
4. **Fai le modifiche** e committale:
   ```bash
   git add .
   git commit -m "feat: descrizione della modifica"
   ```
5. **Pusha** il branch sul tuo fork:
   ```bash
   git push origin feat/nome-della-funzionalita
   ```
6. **Apri una Pull Request** su GitHub verso il branch `main` di questo repository

### Convenzioni per i commit

| Prefisso | Quando usarlo |
|---|---|
| `feat:` | Nuova funzionalità |
| `fix:` | Correzione di un bug |
| `docs:` | Modifiche alla documentazione |
| `style:` | Modifiche CSS/UI senza impatto funzionale |
| `refactor:` | Refactoring del codice |
| `test:` | Aggiunta o modifica di test |

### Segnalare un bug

Apri una **Issue** su GitHub con:
- Versione di Odoo utilizzata
- Descrizione del problema
- Passi per riprodurlo
- Screenshot (se utile)

### Suggerire una funzionalità

Apri una **Issue** con il tag `enhancement` descrivendo la funzionalità desiderata e il caso d'uso.

### Linee guida

- Il codice deve essere compatibile con **Odoo 18**
- Segui le convenzioni di naming di Odoo (snake_case per Python, kebab-case per XML id)
- Testa il modulo su un'installazione pulita prima di aprire la PR
- Aggiorna il `README.md` se aggiungi nuove funzionalità

---

*Grazie a tutti coloro che contribuiscono a migliorare questo progetto!* 🙏
