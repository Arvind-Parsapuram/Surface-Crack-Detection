import base64

from ui.config import ICONS, ACCENT, SEVERITY_COLOR
from ui.utils import compute_stats
from ui.html_builders import stat_card_html


def refresh_user(user, history):
    total, cracks, no_cracks, avg_conf = compute_stats(history)
    name = user.get("full_name", "User")
    email = user.get("email", "")
    initial = name[0].upper() if name else "U"

    stats = f"""<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.75rem;">
    {stat_card_html(ICONS["image"], ACCENT, "Analyses Performed", total)}
    {stat_card_html(ICONS["warning"], "#e74c3c", "Cracks Detected", cracks)}
    {stat_card_html(ICONS["check"], "#2ecc71", "No Cracks", no_cracks)}
    {stat_card_html(ICONS["target"], "#3498db", "Avg. Confidence", f"{avg_conf:.1%}")}
    </div>"""

    profile = f"""<div class="card" style="text-align:center;">
    <div class="sidebar-user-avatar" style="width:56px;height:56px;font-size:1.3rem;margin:0 auto 0.75rem;">{initial}</div>
    <div class="card-title" style="margin-bottom:0.25rem;">{name}</div>
    <p style="color:var(--text-secondary);font-size:0.85rem;margin:0;">{email}</p>
    <span class="severity-badge" style="background:var(--accent-glow);color:var(--accent);border:1px solid var(--accent);margin-top:0.5rem;">Developer</span>
    </div>"""

    activity = f'<div class="card"><div class="card-header">{ICONS["clock"]}<div class="card-title">Recent Activity</div></div>'
    if history:
        for h in history[:5]:
            thumb = h.get("thumbnail")
            img_html = ""
            if thumb:
                b64 = base64.b64encode(thumb).decode()
                img_html = f'<img class="act-thumb" src="data:image/jpeg;base64,{b64}">'
            sev = h.get("severity_label", "---")
            sev_color = SEVERITY_COLOR.get(sev, "#999")
            activity += f"""<div class="act-item">
            {img_html}
            <div class="act-info"><div class="act-class">{h["predicted_class"]}</div><div class="act-meta">{h["confidence"]:.1%} confidence</div></div>
            <span class="pill" style="background:{sev_color};">{sev}</span>
            <div class="act-time">{h.get("timestamp", "")}</div>
            </div>"""
    else:
        activity += '<div class="card-desc">No activity yet.</div>'
    activity += "</div>"

    return stats, profile, activity
