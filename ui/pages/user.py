import gradio as gr

from ui.config import ICONS


def build_user_page():
    with gr.Column(visible=False) as user_page:
        gr.HTML('<div class="page-title">User</div>')
        gr.HTML('<div class="page-sub">Manage your profile and account settings.</div>')
        with gr.Row(equal_height=False):
            with gr.Column(scale=1):
                user_profile = gr.HTML(f'<div class="card"><div class="card-header">{ICONS["user"]}<div class="card-title">Profile</div></div><div class="card-desc">Loading...</div></div>')
            with gr.Column(scale=1):
                user_stats = gr.HTML(f'<div class="card"><div class="card-header">{ICONS["chart"]}<div class="card-title">Statistics</div></div><div class="card-desc">Loading...</div></div>')
        user_activity = gr.HTML(f'<div class="card"><div class="card-header">{ICONS["clock"]}<div class="card-title">Recent Activity</div></div><div class="card-desc">No activity yet.</div></div>')

    return {
        "page": user_page,
        "profile": user_profile,
        "stats": user_stats,
        "activity": user_activity,
    }
