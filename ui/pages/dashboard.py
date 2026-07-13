import gradio as gr

from ui.config import ICONS


def build_dashboard_page():
    with gr.Column(visible=True) as dashboard_page:
        gr.HTML('<div class="page-title">Dashboard</div>')
        gr.HTML('<div class="page-sub">Upload an image to detect and analyze surface defects.</div>')
        dash_stats = gr.HTML("")
        with gr.Row(equal_height=False):
            with gr.Column(scale=1):
                gr.HTML(f'<div class="card"><div class="card-header">{ICONS["upload"]}<div class="card-title">Upload &amp; Predict</div></div><div class="card-desc">Upload a road or bridge surface image to detect defects.</div></div>')
                dash_upload = gr.Image(type="pil", height=300, show_label=False, container=False)
                dash_run = gr.Button("Run Prediction", variant="primary", size="lg")
            with gr.Column(scale=1):
                dash_recent = gr.HTML(f'<div class="card"><div class="card-header">{ICONS["image"]}<div class="card-title">Recent Prediction</div></div><div class="card-desc">No predictions yet. Upload an image above.</div></div>')
        with gr.Row(equal_height=False):
            with gr.Column(scale=1):
                gr.HTML(f'<div class="card" style="padding-bottom:1rem;"><div class="card-header">{ICONS["chart"]}<div class="card-title">Class Distribution</div></div></div>')
                dash_chart = gr.Plot(None, show_label=False, container=False)
            with gr.Column(scale=1):
                dash_severity = gr.HTML(f'<div class="card"><div class="card-header">{ICONS["warning"]}<div class="card-title">Severity Overview</div></div><div class="card-desc">No data yet.</div></div>')

    return {
        "page": dashboard_page,
        "stats": dash_stats,
        "upload": dash_upload,
        "run": dash_run,
        "recent": dash_recent,
        "chart": dash_chart,
        "severity": dash_severity,
    }
