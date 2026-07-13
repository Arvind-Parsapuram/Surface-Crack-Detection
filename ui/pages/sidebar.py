"""
Sidebar Component - Updated for unified routing system

Builds the sidebar with navigation buttons that work with the new routing.
"""

import gradio as gr

from ui.config import ICONS
from ui.routing import get_nav_items


def build_sidebar():
    with gr.Column(scale=1, elem_classes="sidebar", min_width=220):
        with gr.Column(elem_classes="sidebar-inner"):
            gr.HTML(f'<div class="app-logo">{ICONS["road"]} Surface Crack Detection</div>')
            gr.HTML('<div class="app-tagline">Detect & analyze road surface cracks</div>')
            
            # Build nav buttons from routing config
            nav_items = get_nav_items()
            nav_buttons_html = ''.join(
                f'<button class="nav-btn {"active" if i == 0 else ""}" data-page="{item.name}">'
                f'{ICONS[item.icon]} {item.label}</button>'
                for i, item in enumerate(nav_items)
            )
            
            gr.HTML(
                f'<div class="nav-group">'
                f'{nav_buttons_html}'
                f'</div>'
            )
            
            # Hidden state for navigation (synced with URL via JS)
            nav_state = gr.Textbox(value="Dashboard", visible=False, elem_id="nav-state")
            gr.HTML('<div class="sidebar-footer" id="sidebar-footer"></div>')
            user_sidebar_info = gr.HTML("")

    return {
        "nav_state": nav_state,
        "user_sidebar_info": user_sidebar_info,
    }
