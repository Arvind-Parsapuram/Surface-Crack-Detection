import gradio as gr

from ui.config import ICONS


def build_about_page():
    with gr.Column(visible=False) as about_page:
        gr.HTML('<div class="page-title">About Us</div>')
        gr.HTML('<div class="page-sub">Learn more about our project and team.</div>')
        with gr.Row(equal_height=False):
            with gr.Column(scale=3):
                gr.HTML(
                    f'<div class="card">'
                    f'<div class="card-header">{ICONS["star"]}<div class="card-title">Project Overview</div></div>'
                    f'<p style="font-size:0.9rem;color:var(--text-secondary);line-height:1.6;">'
                    f'Surface Crack Detection is an AI-powered application designed to '
                    f'identify and classify surface defects in road and concrete images. '
                    f'The system uses a deep learning model to detect cracks, potholes, '
                    f'patches, and other surface defects with high accuracy.</p>'
                    f'<div class="feature-grid">'
                    f'<div class="feat-card">{ICONS["dashboard"]}<div class="ft">AI Powered</div><div class="fd">Deep learning model for accurate detection</div></div>'
                    f'<div class="feat-card">{ICONS["target"]}<div class="ft">High Accuracy</div><div class="fd">Trained on diverse datasets for reliable results</div></div>'
                    f'<div class="feat-card">{ICONS["check"]}<div class="ft">Easy to Use</div><div class="fd">Simple interface for quick, efficient analysis</div></div>'
                    f'</div>'
                    f'<p style="margin-top:1rem;"><strong style="font-size:0.85rem;">Technologies Used</strong><br>'
                    f'<span class="tech-badge">Python</span> '
                    f'<span class="tech-badge">PyTorch</span> '
                    f'<span class="tech-badge">Gradio</span> '
                    f'<span class="tech-badge">OpenCV</span> '
                    f'<span class="tech-badge">PIL</span> '
                    f'<span class="tech-badge">NumPy</span> '
                    f'<span class="tech-badge">Pandas</span> '
                    f'<span class="tech-badge">Scikit-learn</span></p>'
                    f'</div>'
                )
            with gr.Column(scale=2):
                gr.HTML(
                    f'<div class="card">'
                    f'<div class="card-header">{ICONS["user"]}<div class="card-title">Our Team</div></div>'
                    f'<div class="team-row"><div class="team-av" style="background:#6C5CE7;">AP</div><div><strong>Arvind Parsapuram</strong><br><span style="font-size:0.8rem;color:var(--text-secondary);">Developer &amp; Designer</span></div></div>'
                    f'<div class="team-row"><div class="team-av" style="background:#00b894;">ML</div><div><strong>Team Member</strong><br><span style="font-size:0.8rem;color:var(--text-secondary);">ML Engineer</span></div></div>'
                    f'<div class="team-row"><div class="team-av" style="background:#fdcb6e;color:#333;">DE</div><div><strong>Team Member</strong><br><span style="font-size:0.8rem;color:var(--text-secondary);">Data Engineer</span></div></div>'
                    f'</div>'
                    f'<div class="card">'
                    f'<div class="card-header">{ICONS["dashboard"]}<div class="card-title">Repository</div></div>'
                    f'<p style="font-size:0.85rem;color:var(--text-secondary);">'
                    f'This project is part of the ACE Bootcamp — Team 7.<br>'
                    f'Built with open-source technologies.</p>'
                    f'</div>'
                )

    return {
        "page": about_page,
    }
