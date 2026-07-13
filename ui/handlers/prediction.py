import io
from datetime import datetime

import gradio as gr

from backend.prediction import predict_image
from ui.config import ICONS, SEVERITY_COLOR, ACCENT
from ui.utils import compute_stats, class_distribution, severity_distribution, donut_chart
from ui.html_builders import stat_card_html, recent_card_html, severity_bars_html


def _refresh_dashboard(history):
    total, cracks, no_cracks, avg_conf = compute_stats(history)
    stats = '<div class="stat-grid">' + "".join(
        stat_card_html(icon, bg, label, val)
        for icon, bg, label, val in [
            (ICONS["image"], ACCENT, "Total Analyses", total),
            (ICONS["warning"], "#e74c3c", "Cracks Detected", cracks),
            (ICONS["check"], "#2ecc71", "No Cracks", no_cracks),
            (ICONS["target"], "#3498db", "Avg. Confidence", f"{avg_conf:.1%}"),
        ]
    ) + '</div>'
    recent = recent_card_html(history)
    dist = class_distribution(history)
    chart = donut_chart(dist)
    sev_counts, sev_total = severity_distribution(history)
    severity = severity_bars_html(sev_counts, sev_total)
    return stats, recent, chart, severity


def run_dash_prediction(img, history):
    if img is None:
        return history, gr.update(), gr.update(), gr.update(), gr.update()
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    result = predict_image(image_bytes=buf.getvalue(), filename="upload.jpg")
    if result.get("success"):
        record = {
            "predicted_class": result["predicted_class"],
            "confidence": result["confidence"],
            "class_probabilities": result["class_probabilities"],
            "severity_label": result["severity_label"],
            "severity_score": result["severity_score"],
            "timestamp": datetime.now().strftime("%d %b %Y, %I:%M %p"),
            "thumbnail": buf.getvalue(),
            "filename": "upload.jpg",
        }
        history.insert(0, record)
        stats, recent, chart, severity = _refresh_dashboard(history)
        return history, stats, recent, chart, severity
    return history, gr.update(), gr.update(), gr.update(), gr.update()


def run_predict_prediction(img, selected_class, history):
    if img is None:
        return gr.update(), gr.update()
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    result = predict_image(image_bytes=buf.getvalue(), filename="predict.jpg")
    if not result.get("success"):
        return gr.update(value="<div class='card' style='color:#dc2626;'>Prediction failed.</div>"), gr.update()

    predicted_class = result["predicted_class"]
    confidence = result["confidence"]
    class_probs = result["class_probabilities"]
    severity_label = result["severity_label"]
    severity_score = result["severity_score"]

    record = {
        "predicted_class": predicted_class,
        "confidence": confidence,
        "class_probabilities": class_probs,
        "severity_label": severity_label,
        "severity_score": severity_score,
        "timestamp": datetime.now().strftime("%d %b %Y, %I:%M %p"),
        "thumbnail": buf.getvalue(),
        "filename": "predict.jpg",
    }
    history.insert(0, record)

    sev_color = SEVERITY_COLOR.get(severity_label, "#999")
    sev_icon = ICONS["warning"] if severity_label in ("High", "Critical") else ICONS["check"]
    results_html = f"""<div class="card card-highlight">
    <div class="card-header">{ICONS["check"]}<div class="card-title">Prediction Result</div></div>
    <div style="display:flex;justify-content:space-between;align-items:center;">
    <span style="font-size:1.3rem;font-weight:700;color:var(--accent);">{predicted_class}</span>
    <span style="font-size:1.1rem;font-weight:600;">{confidence:.1%}</span>
    </div>
    </div>
    <div class="card"><div class="card-header">{ICONS["chart"]}<div class="card-title">Class Probabilities</div></div>"""
    for cls, prob in class_probs.items():
        pct = prob * 100
        results_html += f"""<div class="progress-label"><span>{cls}</span><span>{prob:.1%}</span></div>
<div class="progress-track"><div class="progress-fill" style="width:{pct}%;"></div></div>"""
    results_html += f"""</div>
    <div class="card card-highlight" style="border-left-color:{sev_color};">
    <div style="display:flex;justify-content:space-between;align-items:center;">
    <div><span style="font-size:0.85rem;color:var(--text-secondary);">Severity Level</span><br>
    <span class="severity-badge" style="background:{sev_color};color:white;margin-top:4px;">{sev_icon} {severity_label}</span></div>
    <div style="text-align:right;"><span style="font-size:0.85rem;color:var(--text-secondary);">Severity Score</span><br>
    <span style="font-size:1.1rem;font-weight:600;">{severity_score:.2f} / 1.00</span></div>
    </div></div>"""

    report = f"""SURFACE CRACK DETECTION REPORT
===============================
Selected Category: {selected_class}
Predicted Class: {predicted_class}
Confidence: {confidence:.1%}
Severity Level: {severity_label}
Severity Score: {severity_score:.2f}

Class Probabilities:
"""
    for cls, prob in class_probs.items():
        report += f"  {cls}: {prob:.1%}\n"

    report_html = f"""<div class="card">
    <div class="card-header">{ICONS["download"]}<div class="card-title">Final Report</div></div>
    <textarea style="width:100%;height:140px;border:1px solid var(--border-light);border-radius:8px;padding:0.75rem;font-family:monospace;font-size:0.82rem;color:var(--text-primary);background:var(--input-bg);resize:none;" readonly>{report}</textarea>
    <div style="margin-top:0.75rem;"><a href="data:text/plain;charset=utf-8,{report.replace(' ', '%20').replace('\n', '%0A')}" download="final_report.txt" class="dl-btn">{ICONS["download"]} Download Report</a></div>
    </div>"""

    return gr.update(value=results_html), gr.update(value=report_html)
