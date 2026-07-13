import gradio as gr

from ui.config import ICONS, CLASSES


def build_predict_page():
    with gr.Column(visible=False) as predict_page:
        gr.HTML('<div class="page-title">Predict</div>')
        gr.HTML('<div class="page-sub">Run a detailed analysis on a single image.</div>')
        with gr.Row(equal_height=False):
            with gr.Column(scale=1):
                gr.HTML(f'<div class="card"><div class="card-header">{ICONS["upload"]}<div class="card-title">Select &amp; Upload</div></div></div>')
                pred_class_selector = gr.Radio(CLASSES, value=CLASSES[0], label="Expected category", container=False)
                pred_upload = gr.Image(type="pil", height=300, show_label=False, container=False)
                pred_run = gr.Button("Run Prediction", variant="primary", size="lg")
            with gr.Column(scale=1):
                pred_results = gr.HTML(f'<div class="card"><div class="card-header">{ICONS["check"]}<div class="card-title">Results</div></div><div class="card-desc">Run a prediction to see results here.</div></div>')
        pred_report = gr.HTML("")

    return {
        "page": predict_page,
        "class_selector": pred_class_selector,
        "upload": pred_upload,
        "run": pred_run,
        "results": pred_results,
        "report": pred_report,
    }
