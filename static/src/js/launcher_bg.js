/** @odoo-module **/

import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

const STYLE_ID = "launcher_dynamic_style";
const LAUNCHER_CLASS = "o_launcher_kanban";

function applySettings(settings) {
    let styleEl = document.getElementById(STYLE_ID);
    if (!styleEl) {
        styleEl = document.createElement("style");
        styleEl.id = STYLE_ID;
        document.head.appendChild(styleEl);
    }
    const fontSize = parseInt(settings.label_font_size) || 15;
    const iconPx = parseInt(settings.icon_px) || 130;
    const recordPx = iconPx + 10; // record leggermente più largo dell'icona

    styleEl.textContent = `
        .o_launcher_kanban,
        .o_launcher_kanban .o_kanban_renderer {
            background: ${settings.background_color} !important;
        }
        .o_launcher_kanban .o_kanban_record {
            width: ${recordPx}px !important;
            min-width: ${recordPx}px !important;
            max-width: ${recordPx}px !important;
            flex: 0 0 ${recordPx}px !important;
        }
        .o_launcher_kanban .o_launch_icon {
            background: ${settings.icon_bg_color} !important;
            width: ${iconPx}px !important;
            height: ${iconPx}px !important;
            border-radius: ${Math.round(iconPx * 0.18)}px !important;
        }
        .o_launcher_kanban .o_launch_icon img {
            width: ${iconPx}px !important;
            height: ${iconPx}px !important;
        }
        .o_launcher_kanban .o_launch_icon i {
            font-size: ${Math.round(iconPx * 0.4)}px !important;
        }
        .o_launcher_kanban .o_launch_label {
            color: ${settings.label_color} !important;
            font-size: ${fontSize}px !important;
        }
    `;
}

async function fetchAndApply() {
    try {
        const settings = await rpc("/web/dataset/call_kw/launcher.settings/get_settings", {
            model: "launcher.settings",
            method: "get_settings",
            args: [],
            kwargs: {},
        });
        if (settings) {
            applySettings(settings);
        }
    } catch (e) {
        console.warn("LauncherBG: impossibile leggere le impostazioni", e);
    }
}

const observer = new MutationObserver(() => {
    if (document.querySelector(`.${LAUNCHER_CLASS}`)) {
        fetchAndApply();
    }
});

registry.category("services").add("launcher_bg_service", {
    start() {
        fetchAndApply();
        observer.observe(document.body, { childList: true, subtree: true });
    },
});
