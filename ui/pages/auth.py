"""
Auth Pages - Updated for unified routing system

Builds the authentication section with landing, login, register, and forgot password pages.
Uses auth_nav_state for internal navigation and route_state for URL synchronization.
"""

import gradio as gr

from ui.config import ICONS


def build_auth_section():
    with gr.Column(elem_classes="auth-container", visible=True) as auth_section:

        # Hidden state for auth navigation (synced with URL via JS)
        auth_nav_state = gr.Textbox(value="landing", visible=False, elem_id="auth-nav-state")

        # =====================================================================
        # LANDING PAGE
        # =====================================================================
        with gr.Column(elem_classes="auth-box", visible=True) as landing_col:
            gr.HTML(
                '<div class="landing-hero">'
                f'<div class="landing-road-icon">{ICONS["road"]}</div>'
                '<div class="landing-title">Surface Crack Detection</div>'
                '<div class="landing-desc">AI-powered detection and classification of road and bridge surface defects using Deep Learning and Computer Vision.</div>'
                f'<div class="landing-features">'
                f'<span class="landing-feat-chip">{ICONS["star"]} AI-Powered</span>'
                f'<span class="landing-feat-chip">{ICONS["target"]} 80% Accuracy</span>'
                f'<span class="landing-feat-chip">{ICONS["dashboard"]} Real-Time</span>'
                f'</div>'
                '</div>'
            )
            go_login_btn = gr.Button("Login", variant="primary", size="lg", elem_id="go-login-btn")

        # =====================================================================
        # LOGIN PAGE
        # =====================================================================
        with gr.Column(elem_classes="auth-box", visible=False) as login_col:
            gr.HTML(f'<div class="auth-logo">{ICONS["lock"]}</div>')
            gr.HTML('<div class="auth-title">Welcome Back</div>')
            gr.HTML('<div class="auth-subtitle">Sign in to your account</div>')
            login_error = gr.HTML("", visible=False, elem_classes="auth-error")
            login_email = gr.Textbox(label="Email", placeholder="you@example.com")
            login_password = gr.Textbox(label="Password", placeholder="\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022", type="password")
            login_btn = gr.Button("Sign In", variant="primary", size="lg")
            gr.HTML('<div class="auth-divider">or continue with</div>')
            github_link = gr.HTML("", elem_classes="auth-github-link")
            with gr.Row():
                show_forgot_btn = gr.Button("Forgot Password?", elem_classes="auth-link-btn", elem_id="show-forgot-btn")
                show_register_from_login_btn = gr.Button("Create Account", elem_classes="auth-link-btn", elem_id="show-register-btn")

        # =====================================================================
        # REGISTER PAGE
        # =====================================================================
        with gr.Column(elem_classes="auth-box", visible=False) as register_col:
            gr.HTML(f'<div class="auth-logo">{ICONS["user"]}</div>')
            gr.HTML('<div class="auth-title">Create Account</div>')
            gr.HTML('<div class="auth-subtitle">Join Surface Crack Detection</div>')
            register_msg = gr.HTML("", visible=False)
            reg_name = gr.Textbox(label="Full Name", placeholder="John Doe")
            reg_email = gr.Textbox(label="Email", placeholder="you@example.com")
            reg_phone = gr.Textbox(label="Phone Number", placeholder="+1 234 567 890")
            reg_password = gr.Textbox(label="Password", placeholder="Min. 6 characters", type="password")
            reg_confirm = gr.Textbox(label="Confirm Password", placeholder="\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022", type="password")
            register_btn = gr.Button("Create Account", variant="primary", size="lg")
            back_to_login_btn = gr.Button("Back to Login", elem_classes="auth-link-btn", elem_id="back-to-login-btn")

        # =====================================================================
        # FORGOT PASSWORD PAGE
        # =====================================================================
        with gr.Column(elem_classes="auth-box", visible=False) as forgotpwd_col:
            gr.HTML(f'<div class="auth-logo">{ICONS["lock"]}</div>')
            gr.HTML('<div class="auth-title">Forgot Password</div>')
            gr.HTML('<div class="auth-subtitle">Enter your registered email</div>')
            forgot_msg = gr.HTML("", visible=False)
            forgot_email = gr.Textbox(label="Email Address", placeholder="you@example.com")
            send_reset_btn = gr.Button("Send Reset Link", variant="primary", size="lg")
            back_to_login2_btn = gr.Button("Back to Login", elem_classes="auth-link-btn", elem_id="back-to-login2-btn")

    return {
        "section": auth_section,
        "auth_nav_state": auth_nav_state,
        "landing_col": landing_col,
        "go_login_btn": go_login_btn,
        "login_col": login_col,
        "login_error": login_error,
        "login_email": login_email,
        "login_password": login_password,
        "login_btn": login_btn,
        "github_link": github_link,
        "show_forgot_btn": show_forgot_btn,
        "show_register_from_login_btn": show_register_from_login_btn,
        "register_col": register_col,
        "register_msg": register_msg,
        "reg_name": reg_name,
        "reg_email": reg_email,
        "reg_phone": reg_phone,
        "reg_password": reg_password,
        "reg_confirm": reg_confirm,
        "register_btn": register_btn,
        "back_to_login_btn": back_to_login_btn,
        "forgotpwd_col": forgotpwd_col,
        "forgot_msg": forgot_msg,
        "forgot_email": forgot_email,
        "send_reset_btn": send_reset_btn,
        "back_to_login2_btn": back_to_login2_btn,
    }
