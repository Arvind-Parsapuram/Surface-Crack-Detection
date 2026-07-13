import gradio as gr

from backend.auth import login_user, register_user, send_reset_email, get_github_login_url, complete_github_login
from ui.config import APP_URL, ICONS

_GITHUB_LOGIN_URL = None


def _get_github_url():
    global _GITHUB_LOGIN_URL
    if _GITHUB_LOGIN_URL is None:
        try:
            _GITHUB_LOGIN_URL = get_github_login_url(redirect_to=APP_URL)
        except Exception:
            _GITHUB_LOGIN_URL = "#"
    return _GITHUB_LOGIN_URL


def handle_login(email, password):
    if not email or not password:
        return gr.update(visible=True, value="Please enter both email and password."), None, {}
    try:
        result = login_user(email=email, password=password)
        if result.get("success"):
            return gr.update(visible=False), result["access_token"], result["user"]
        return gr.update(visible=True, value=result.get("message", "Invalid credentials")), None, {}
    except Exception as e:
        return gr.update(visible=True, value=str(e)), None, {}


def after_login_success(token, user):
    if token:
        return gr.update(visible=False), gr.update(visible=True)
    return gr.update(), gr.update()


def handle_register(name, email, phone, password, confirm):
    if not name or not email or not password:
        return gr.update(visible=True, value="Please fill in all required fields.")
    if password != confirm:
        return gr.update(visible=True, value="Passwords do not match.")
    if len(password) < 6:
        return gr.update(visible=True, value="Password must be at least 6 characters.")
    try:
        result = register_user(email=email, password=password, full_name=name)
        if result.get("success"):
            return gr.update(visible=True, value=f'{ICONS["check"]} ' + result.get("message", "Registration successful! Please check your email."))
        return gr.update(visible=True, value="Registration failed.")
    except Exception as e:
        return gr.update(visible=True, value=str(e))


def handle_forgot(email):
    if not email:
        return gr.update(visible=True, value="Please enter your email address.")
    try:
        result = send_reset_email(email=email)
        if result.get("success"):
            return gr.update(visible=True, value=f'{ICONS["check"]} ' + result.get("message", "Reset link sent."))
        return gr.update(visible=True, value="Failed to send reset link.")
    except Exception as e:
        return gr.update(visible=True, value=str(e))


def gen_github_link():
    url = _get_github_url()
    return f'<a href="{url}">{ICONS["github"]} Login with GitHub</a>'


def check_oauth(request: gr.Request):
    code = request.query_params.get("code")
    if code:
        try:
            result = complete_github_login(code)
            if result.get("success"):
                return result["access_token"], result["user"], gr.update(visible=False), gr.update(visible=True)
        except Exception:
            pass
    return None, {}, gr.update(), gr.update()
