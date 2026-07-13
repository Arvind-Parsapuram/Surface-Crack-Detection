"""
Unified Routing System for Gradio App

Centralizes all route definitions, path mappings, and navigation logic.
Replaces the scattered routing in navigation.py, assembly.py, and JavaScript.
"""

from enum import Enum
from typing import Dict, List, Optional, Literal
from dataclasses import dataclass


class AuthRoute(str, Enum):
    """Authentication flow routes (public, no auth required)"""
    LANDING = "/"
    LOGIN = "/login"
    REGISTER = "/register"
    FORGOT = "/forgot"
    OAUTH_CALLBACK = "/auth/callback"


class AppRoute(str, Enum):
    """Main application routes (require authentication)"""
    DASHBOARD = "/dashboard"
    PREDICT = "/predict"
    USER = "/user"
    ABOUT = "/about"
    LOGOUT = "/logout"


class RouteType(str, Enum):
    AUTH = "auth"
    APP = "app"


@dataclass(frozen=True)
class RouteConfig:
    """Configuration for a single route"""
    path: str
    name: str
    route_type: RouteType
    requires_auth: bool
    icon: str
    label: str
    order: int


# =============================================================================
# ROUTE REGISTRY - Single source of truth for all routes
# =============================================================================

AUTH_ROUTES: List[RouteConfig] = [
    RouteConfig(
        path=AuthRoute.LANDING,
        name="landing",
        route_type=RouteType.AUTH,
        requires_auth=False,
        icon="",
        label="Landing",
        order=0,
    ),
    RouteConfig(
        path=AuthRoute.LOGIN,
        name="login",
        route_type=RouteType.AUTH,
        requires_auth=False,
        icon="",
        label="Login",
        order=1,
    ),
    RouteConfig(
        path=AuthRoute.REGISTER,
        name="register",
        route_type=RouteType.AUTH,
        requires_auth=False,
        icon="",
        label="Register",
        order=2,
    ),
    RouteConfig(
        path=AuthRoute.FORGOT,
        name="forgot",
        route_type=RouteType.AUTH,
        requires_auth=False,
        icon="",
        label="Forgot Password",
        order=3,
    ),
]

APP_ROUTES: List[RouteConfig] = [
    RouteConfig(
        path=AppRoute.DASHBOARD,
        name="Dashboard",
        route_type=RouteType.APP,
        requires_auth=True,
        icon="dashboard",
        label="Dashboard",
        order=0,
    ),
    RouteConfig(
        path=AppRoute.PREDICT,
        name="Predict",
        route_type=RouteType.APP,
        requires_auth=True,
        icon="predict",
        label="Predict",
        order=1,
    ),
    RouteConfig(
        path=AppRoute.USER,
        name="User",
        route_type=RouteType.APP,
        requires_auth=True,
        icon="user",
        label="User",
        order=2,
    ),
    RouteConfig(
        path=AppRoute.ABOUT,
        name="About Us",
        route_type=RouteType.APP,
        requires_auth=True,
        icon="about",
        label="About Us",
        order=3,
    ),
    RouteConfig(
        path=AppRoute.LOGOUT,
        name="Logout",
        route_type=RouteType.APP,
        requires_auth=True,
        icon="logout",
        label="Logout",
        order=4,
    ),
]

ALL_ROUTES = AUTH_ROUTES + APP_ROUTES

# =============================================================================
# LOOKUP MAPS - Built once at module load
# =============================================================================

_PATH_TO_ROUTE: Dict[str, RouteConfig] = {r.path: r for r in ALL_ROUTES}
_NAME_TO_ROUTE: Dict[str, RouteConfig] = {r.name: r for r in ALL_ROUTES}
_AUTH_PATH_TO_NAME: Dict[str, str] = {r.path: r.name for r in AUTH_ROUTES}
_APP_PATH_TO_NAME: Dict[str, str] = {r.path: r.name for r in APP_ROUTES}
_APP_NAME_TO_PATH: Dict[str, str] = {r.name: r.path for r in APP_ROUTES}


# =============================================================================
# PUBLIC API
# =============================================================================

def get_route_by_path(path: str) -> Optional[RouteConfig]:
    """Get route config by URL path"""
    return _PATH_TO_ROUTE.get(path)


def get_route_by_name(name: str) -> Optional[RouteConfig]:
    """Get route config by route name"""
    return _NAME_TO_ROUTE.get(name)


def is_auth_route(path: str) -> bool:
    """Check if path is an authentication route"""
    return path in _AUTH_PATH_TO_NAME


def is_app_route(path: str) -> bool:
    """Check if path is a main app route"""
    return path in _APP_PATH_TO_NAME


def get_auth_route_name(path: str) -> Optional[str]:
    """Get auth route name from path"""
    return _AUTH_PATH_TO_NAME.get(path)


def get_app_route_name(path: str) -> Optional[str]:
    """Get app route name from path"""
    return _APP_PATH_TO_NAME.get(path)


def get_app_route_path(name: str) -> Optional[str]:
    """Get app route path from name"""
    return _APP_NAME_TO_PATH.get(name)


def get_default_app_route() -> str:
    """Get default app route path (Dashboard)"""
    return AppRoute.DASHBOARD


def get_default_auth_route() -> str:
    """Get default auth route path (Landing)"""
    return AuthRoute.LANDING


def get_nav_items() -> List[RouteConfig]:
    """Get navigation items for sidebar (app routes only, in order)"""
    return sorted(APP_ROUTES, key=lambda r: r.order)


def get_auth_nav_items() -> List[RouteConfig]:
    """Get auth navigation items in order"""
    return sorted(AUTH_ROUTES, key=lambda r: r.order)


# =============================================================================
# JAVASCRIPT ROUTE CONFIG - Serialized for frontend
# =============================================================================

def get_js_route_config() -> dict:
    """Get route configuration serialized for JavaScript"""
    return {
        "authRoutes": {
            r.name: r.path for r in AUTH_ROUTES
        },
        "appRoutes": {
            r.name: r.path for r in APP_ROUTES
        },
        "pathToAuth": {r.path: r.name for r in AUTH_ROUTES},
        "pathToApp": {r.path: r.name for r in APP_ROUTES},
        "defaultAuthPath": AuthRoute.LANDING,
        "defaultAppPath": AppRoute.DASHBOARD,
    }


# =============================================================================
# NAVIGATION HELPERS
# =============================================================================

def navigate_to_auth(route_name: str) -> str:
    """Get path for auth navigation"""
    route = get_route_by_name(route_name)
    if route and route.route_type == RouteType.AUTH:
        return route.path
    return AuthRoute.LANDING


def navigate_to_app(route_name: str) -> str:
    """Get path for app navigation"""
    route = get_route_by_name(route_name)
    if route and route.route_type == RouteType.APP:
        return route.path
    return AppRoute.DASHBOARD


def get_route_state(path: str) -> dict:
    """
    Determine the complete route state from a URL path.
    Returns dict with keys: is_auth, route_name, route_type, requires_auth
    """
    route = get_route_by_path(path)
    if not route:
        # Unknown path - default to landing if not authenticated context
        return {
            "is_auth": True,
            "route_name": "landing",
            "route_type": RouteType.AUTH,
            "requires_auth": False,
            "path": AuthRoute.LANDING,
        }
    
    return {
        "is_auth": route.route_type == RouteType.AUTH,
        "route_name": route.name,
        "route_type": route.route_type,
        "requires_auth": route.requires_auth,
        "path": route.path,
    }