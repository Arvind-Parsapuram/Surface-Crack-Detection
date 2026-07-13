import gradio as gr

from ui.config import ICONS


def build_logout_modal():
    with gr.Column(visible=False) as logout_modal:
        gr.HTML(
            f'<div class="modal-overlay">'
            f'<div class="modal-box">'
            f'<div style="display:flex;justify-content:center;margin-bottom:0.75rem;">{ICONS["logout"]}</div>'
            f'<h3 style="margin:0 0 0.25rem;">Logout</h3>'
            f'<p style="color:var(--text-secondary);font-size:0.9rem;margin:0 0 1.5rem;">Are you sure you want to logout?</p>'
            f'</div></div>'
        )
        with gr.Row():
            cancel_logout_btn = gr.Button("Cancel", size="lg")
            confirm_logout_btn = gr.Button("Yes, Logout", variant="primary", size="lg")

    return {
        "modal": logout_modal,
        "cancel_btn": cancel_logout_btn,
        "confirm_btn": confirm_logout_btn,
    }
