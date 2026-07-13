"""
Navigation Handlers - Updated for unified routing system

Handles all navigation logic for both auth and app sections.
Uses the centralized routing configuration from ui.routing.
"""

import gradio as gr

from ui.routing import (
    AuthRoute, AppRoute, RouteType,
    get_route_by_path, get_route_by_name,
    is_auth_route, is_app_route,
    get_auth_route_name, get_app_route_name,
    get_default_app_route, get_default_auth_route,
    get_nav_items, get_auth_nav_items,
    navigate_to_auth, navigate_to_app,
    get_route_state,
)


# =============================================================================
# AUTH NAVIGATION
# =============================================================================

AUTH_PAGE_ORDER = ["landing", "login", "register", "forgot"]


def auth_navigate(state: str):
    """Handle auth page navigation (landing, login, register, forgot)"""
    idx = AUTH_PAGE_ORDER.index(state) if state in AUTH_PAGE_ORDER else 0
    return [
        gr.update(visible=(idx == 0)),  # landing
        gr.update(visible=(idx == 1)),  # login
        gr.update(visible=(idx == 2)),  # register
        gr.update(visible=(idx == 3)),  # forgot
        state,  # auth_nav_state
        navigate_to_auth(state),  # route_state
    ]


def show_landing():
    return auth_navigate("landing")


def show_login():
    return auth_navigate("login")


def show_register():
    return auth_navigate("register")


def show_forgot():
    return auth_navigate("forgot")


# =============================================================================
# MAIN APP NAVIGATION
# =============================================================================

def navigate(choice: str, user: dict):
    """
    Handle main app navigation (Dashboard, Predict, User, About, Logout).
    Returns visibility updates for all pages + sidebar info + nav_state + route_state
    """
    if "Logout" in choice:
        # Show logout modal
        return [
            gr.update(visible=False),  # dashboard
            gr.update(visible=False),  # predict
            gr.update(visible=False),  # user
            gr.update(visible=False),  # about
            gr.update(visible=True),   # logout modal
            gr.update(),               # user_sidebar_info (unchanged)
            "Login",                   # nav_state (reset to default)
            "/logout",                 # route_state
        ]

    # Determine which page to show
    dash_v = "Dashboard" in choice
    pred_v = "Predict" in choice
    user_v = "User" in choice
    about_v = "About" in choice

    # Build user sidebar info
    name = user.get("full_name", "User")
    email = user.get("email", "")
    initial = name[0].upper() if name else "U"
    user_sidebar = (
        f'<div style="display:flex;align-items:center;gap:0.6rem;">'
        f'<div class="sidebar-user-avatar">{initial}</div>'
        f'<div><div class="sidebar-user-name">{name}</div>'
        f'<div class="sidebar-user-email">{email}</div></div></div>'
    )

    path = navigate_to_app(choice)

    return [
        gr.update(visible=dash_v),
        gr.update(visible=pred_v),
        gr.update(visible=user_v),
        gr.update(visible=about_v),
        gr.update(visible=False),  # logout modal
        user_sidebar,
        choice,                    # nav_state
        path,                      # route_state
    ]


def cancel_logout():
    """Cancel logout - return to Dashboard"""
    return [
        gr.update(visible=True),   # dashboard
        gr.update(visible=False),  # predict
        gr.update(visible=False),  # user
        gr.update(visible=False),  # about
        gr.update(visible=False),  # logout modal
        "Dashboard",               # nav_state
        "/dashboard",              # route_state
    ]


def do_logout():
    """Confirm logout - clear all state and return to landing"""
    return [
        None,                      # auth_token
        {},                        # user_info
        gr.update(visible=False),  # app_section
        gr.update(visible=True),   # auth_section
        gr.update(visible=True),   # landing_col
        gr.update(visible=False),  # login_col
        gr.update(visible=False),  # register_col
        gr.update(visible=False),  # forgotpwd_col
        "Dashboard",               # nav_state (reset)
        "/",                       # route_state (landing)
    ]


# =============================================================================
# DEEP LINKING / ROUTE RESOLUTION
# =============================================================================

def resolve_route_state(path: str, user_info: dict):
    """
    Resolve complete UI state from a URL path.
    This is called when route_state changes (browser back/forward, deep link).
    
    Returns all UI state needed to render the correct page.
    """
    route = get_route_by_path(path)
    
    if not route:
        # Unknown path - default to landing
        return _get_default_auth_state()
    
    if route.route_type == RouteType.AUTH:
        return _resolve_auth_route(route, path)
    else:
        return _resolve_app_route(route, path, user_info)


def _resolve_auth_route(route, path: str):
    """Resolve UI state for auth routes"""
    auth_state = route.name
    auth_path = route.path
    
    # Visibility for auth pages
    idx = AUTH_PAGE_ORDER.index(auth_state) if auth_state in AUTH_PAGE_ORDER else 0
    auth_vis = [
        gr.update(visible=(idx == 0)),  # landing
        gr.update(visible=(idx == 1)),  # login
        gr.update(visible=(idx == 2)),  # register
        gr.update(visible=(idx == 3)),  # forgot
    ]
    
    return [
        gr.update(visible=True),   # auth_section
        gr.update(visible=False),  # app_section
        *auth_vis,                 # landing, login, register, forgot
        gr.update(visible=False),  # dashboard
        gr.update(visible=False),  # predict
        gr.update(visible=False),  # user
        gr.update(visible=False),  # about
        gr.update(visible=False),  # logout modal
        gr.update(),               # user_sidebar_info (unchanged)
        "Dashboard",               # nav_state (reset)
        auth_state,                # auth_nav_state
        auth_path,                 # route_state
    ]


def _resolve_app_route(route, path: str, user_info: dict):
    """Resolve UI state for app routes"""
    page_name = route.name
    
    # Check if user is authenticated
    is_authenticated = bool(user_info and user_info.get("email"))
    
    if not is_authenticated:
        # Not logged in - redirect to login
        return _get_login_redirect_state()
    
    # Build user sidebar info
    name = user_info.get("full_name", "User")
    email = user_info.get("email", "")
    initial = name[0].upper() if name else "U"
    user_sidebar = (
        f'<div style="display:flex;align-items:center;gap:0.6rem;">'
        f'<div class="sidebar-user-avatar">{initial}</div>'
        f'<div><div class="sidebar-user-name">{name}</div>'
        f'<div class="sidebar-user-email">{email}</div></div></div>'
    )
    
    # Page visibility
    dash_v = page_name == "Dashboard"
    pred_v = page_name == "Predict"
    user_v = page_name == "User"
    about_v = page_name == "About Us"
    logout_v = page_name == "Logout"
    
    return [
        gr.update(visible=False),  # auth_section
        gr.update(visible=True),   # app_section
        gr.update(visible=False),  # landing
        gr.update(visible=False),  # login
        gr.update(visible=False),  # register
        gr.update(visible=False),  # forgot
        gr.update(visible=dash_v), # dashboard
        gr.update(visible=pred_v), # predict
        gr.update(visible=user_v), # user
        gr.update(visible=about_v),# about
        gr.update(visible=logout_v), # logout modal
        user_sidebar,              # user_sidebar_info
        page_name,                 # nav_state
        route.name,                # auth_nav_state (reset)
        path,                      # route_state
    ]


def _get_default_auth_state():
    """Get default state for unknown paths (landing page)"""
    return [
        gr.update(visible=True),   # auth_section
        gr.update(visible=False),  # app_section
        gr.update(visible=True),   # landing
        gr.update(visible=False),  # login
        gr.update(visible=False),  # register
        gr.update(visible=False),  # forgot
        gr.update(visible=False),  # dashboard
        gr.update(visible=False),  # predict
        gr.update(visible=False),  # user
        gr.update(visible=False),  # about
        gr.update(visible=False),  # logout modal
        gr.update(),               # user_sidebar_info
        "Dashboard",               # nav_state
        "landing",                 # auth_nav_state
        "/",                       # route_state
    ]


def _get_login_redirect_state():
    """Get state for redirecting to login when not authenticated"""
    return [
        gr.update(visible=True),   # auth_section
        gr.update(visible=False),  # app_section
        gr.update(visible=False),  # landing
        gr.update(visible=True),   # login
        gr.update(visible=False),  # register
        gr.update(visible=False),  # forgot
        gr.update(visible=False),  # dashboard
        gr.update(visible=False),  # predict
        gr.update(visible=False),  # user
        gr.update(visible=False),  # about
        gr.update(visible=False),  # logout modal
        gr.update(),               # user_sidebar_info
        "Dashboard",               # nav_state
        "login",                   # auth_nav_state
        "/login",                  # route_state
    ]


def get_initial_auth_state():
    """Get initial auth state for app load"""
    return "landing", "/"


def get_initial_app_state():
    """Get initial app state for app load"""
    return "Dashboard", "/dashboard"
