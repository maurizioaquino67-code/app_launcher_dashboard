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
    styleEl.textContent = `
        .o_launcher_kanban,
        .o_launcher_kanban .o_kanban_renderer {
            background: ${settings.background_color} !important;
        }
        .o_launcher_kanban .o_launch_icon {
            background: ${settings.icon_bg_color} !important;
        }
        .o_launcher_kanban .o_launch_label {
            color: ${settings.label_color} !important;
            font-size: ${fontSize}px !important;
        }
    `;
}

async function fetchAndApply() {
    try {
        const settings = await rpc("/web/dataset/call_kw", {
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
