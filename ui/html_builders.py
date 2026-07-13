import base64

from .config import ICONS, SEVERITY_ORDER, SEVERITY_COLOR


def stat_card_html(icon_svg, icon_bg, label, value):
    return f"""<div class="stat-card">
    <div class="stat-icon-wrap" style="background:{icon_bg}18;">{icon_svg}</div>
    <div class="stat-value">{value}</div>
    <div class="stat-label">{label}</div>
    <div style="position:absolute;top:0;left:0;right:0;height:3px;background:{icon_bg};border-radius:16px 16px 0 0;"></div>
</div>"""


def severity_bars_html(counts, total_):
    html = f'<div class="card"><div class="card-header">{ICONS["warning"]}<div class="card-title">Severity Overview</div></div>'
    for sev in SEVERITY_ORDER:
        n = counts.get(sev, 0)
        pct = (n / total_ * 100) if total_ else 0
        html += f"""<div class="progress-label"><span>{sev}</span><span>{n}</span></div>
<div class="progress-track"><div class="progress-fill" style="width:{pct}%;background:{SEVERITY_COLOR.get(sev, '#999')};"></div></div>"""
    html += "</div>"
    return html


def recent_card_html(history):
    if not history:
        return f'<div class="card"><div class="card-header">{ICONS["image"]}<div class="card-title">Recent Prediction</div></div><div class="card-desc">No predictions yet. Upload an image above.</div></div>'
    latest = history[0]
    sev = latest.get("severity_label", "---")
    sev_color = SEVERITY_COLOR.get(sev, "#999")
    thumb = latest.get("thumbnail")
    img_html = ""
    if thumb:
        b64 = base64.b64encode(thumb).decode()
        img_html = f'<img src="data:image/jpeg;base64,{b64}" style="width:100%; border-radius:10px; margin-bottom:0.75rem;box-shadow:var(--shadow-sm);">'
    sev_icon = ICONS["check"] if sev in ("Low", "---") else ICONS["warning"]
    return f"""<div class="card">
    <div class="card-header">{ICONS["image"]}<div class="card-title">Recent Prediction</div></div>
    <div style="position:relative;">
    {img_html}
    <span class="severity-badge" style="position:absolute;top:12px;right:12px;background:{sev_color};color:white;">{sev_icon} {sev}</span>
    </div>
    <div style="display:flex;justify-content:space-between;align-items:center;margin-top:0.5rem;">
    <div><strong style="font-size:1rem;">{latest["predicted_class"]}</strong><br>
    <span style="color:var(--text-secondary);font-size:0.82rem;">{latest["confidence"]:.1%} confidence</span></div>
    <span style="color:var(--text-muted);font-size:0.75rem;">{latest.get("timestamp", "")}</span>
    </div></div>"""
