"""
Main Gradio App Assembly - Updated with unified routing system

This module creates the complete Gradio Blocks application with:
- Unified routing state (single source of truth)
- Event-driven JavaScript routing (no polling)
- Clean separation of auth and app sections
- Proper deep linking support
"""

import gradio as gr

from ui.config import CUSTOM_CSS
from ui.pages.auth import build_auth_section
from ui.pages.sidebar import build_sidebar
from ui.pages.dashboard import build_dashboard_page
from ui.pages.predict import build_predict_page
from ui.pages.user import build_user_page
from ui.pages.about import build_about_page
from ui.pages.logout import build_logout_modal
from ui.handlers.auth import (
    handle_login, after_login_success, handle_register, handle_forgot,
    gen_github_link, check_oauth
)
from ui.handlers.navigation import (
    auth_navigate, show_login, show_register, show_forgot, show_landing,
    navigate, cancel_logout, do_logout, resolve_route_state,
    get_initial_auth_state, get_initial_app_state
)
from ui.handlers.prediction import run_dash_prediction, _refresh_dashboard
from ui.handlers.prediction import run_predict_prediction
from ui.handlers.user import refresh_user


# =============================================================================
# EVENT-DRIVEN JAVASCRIPT ROUTING (No Polling!)
# =============================================================================

NAV_JS = """
<script>
(function() {
    'use strict';

    // Route configuration - single source of truth
    const ROUTES = {
        // Auth routes
        '/': { type: 'auth', name: 'landing' },
        '/login': { type: 'auth', name: 'login' },
        '/register': { type: 'auth', name: 'register' },
        '/forgot': { type: 'auth', name: 'forgot' },
        // App routes
        '/dashboard': { type: 'app', name: 'Dashboard' },
        '/predict': { type: 'app', name: 'Predict' },
        '/user': { type: 'app', name: 'User' },
        '/about': { type: 'app', name: 'About Us' },
        '/logout': { type: 'app', name: 'Logout' },
    };

    const REVERSE_ROUTES = {
        auth: { landing: '/', login: '/login', register: '/register', forgot: '/forgot' },
        app: { Dashboard: '/dashboard', Predict: '/predict', User: '/user', 'About Us': '/about', Logout: '/logout' }
    };

    // DOM element references (cached after init)
    let elements = {
        routeState: null,      // #route-state input
        navState: null,        // #nav-state input
        authNavState: null,    // #auth-nav-state input
        navGroup: null,        // .nav-group
        navButtons: null,      // .nav-btn
    };

    // Initialization flag
    let initialized = false;
    let isNavigating = false;  // Prevent circular updates

    // =========================================================================
    // CORE ROUTING FUNCTIONS
    // =========================================================================

    function getRouteInfo(path) {
        return ROUTES[path] || ROUTES['/'];
    }

    function updateURL(path) {
        if (window.location.pathname !== path) {
            window.history.pushState(null, '', path);
        }
    }

    function setGradioValue(element, value) {
        if (!element) return;
        const nativeSetter = Object.getOwnPropertyDescriptor(
            window.HTMLInputElement.prototype, 'value'
        ).set;
        nativeSetter.call(element, value);
        element.dispatchEvent(new Event('input', { bubbles: true }));
    }

    function setActiveNavButton(pageName) {
        if (!elements.navButtons) return;
        elements.navButtons.forEach(btn => {
            const isActive = btn.getAttribute('data-page') === pageName;
            btn.classList.toggle('active', isActive);
        });
    }

    // =========================================================================
    // GRADIO STATE -> URL (Outbound)
    // =========================================================================

    function onRouteStateChange() {
        if (isNavigating || !elements.routeState) return;
        
        const path = elements.routeState.value;
        if (path && path !== window.location.pathname) {
            updateURL(path);
        }
    }

    function onNavStateChange() {
        if (isNavigating || !elements.navState) return;
        
        const pageName = elements.navState.value;
        const path = REVERSE_ROUTES.app[pageName];
        if (path) {
            setActiveNavButton(pageName);
            updateURL(path);
            // Also update route-state to keep in sync
            if (elements.routeState) {
                setGradioValue(elements.routeState, path);
            }
        }
    }

    function onAuthNavStateChange() {
        if (isNavigating || !elements.authNavState) return;
        
        const authName = elements.authNavState.value;
        const path = REVERSE_ROUTES.auth[authName];
        if (path) {
            updateURL(path);
            if (elements.routeState) {
                setGradioValue(elements.routeState, path);
            }
        }
    }

    // =========================================================================
    // URL -> GRADIO STATE (Inbound) - Browser Back/Forward & Deep Links
    // =========================================================================

    function handlePopState() {
        const path = window.location.pathname || '/';
        const route = getRouteInfo(path);
        
        isNavigating = true;
        
        if (route.type === 'auth') {
            // Update auth nav state
            if (elements.authNavState) {
                setGradioValue(elements.authNavState, route.name);
            }
        } else {
            // Update app nav state
            if (elements.navState) {
                setGradioValue(elements.navState, route.name);
            }
            setActiveNavButton(route.name);
        }
        
        // Always update route-state as the single source of truth
        if (elements.routeState) {
            setGradioValue(elements.routeState, path);
        }
        
        // Reset flag after event loop
        setTimeout(() => { isNavigating = false; }, 0);
    }

    // =========================================================================
    // SIDEBAR CLICK HANDLING
    // =========================================================================

    function setupSidebarClicks() {
        if (!elements.navGroup) return;
        
        elements.navGroup.addEventListener('click', (e) => {
            const btn = e.target.closest('.nav-btn');
            if (!btn) return;
            
            const pageName = btn.getAttribute('data-page');
            if (!pageName) return;
            
            isNavigating = true;
            
            // Update nav-state (triggers Gradio navigation handler)
            if (elements.navState) {
                setGradioValue(elements.navState, pageName);
            }
            
            // Update active button immediately for UX
            setActiveNavButton(pageName);
            
            // Update URL
            const path = REVERSE_ROUTES.app[pageName];
            if (path) {
                updateURL(path);
                if (elements.routeState) {
                    setGradioValue(elements.routeState, path);
                }
            }
            
            setTimeout(() => { isNavigating = false; }, 0);
        });
    }

    // =========================================================================
    // INITIALIZATION
    // =========================================================================

    function cacheElements() {
        elements.routeState = document.querySelector('#route-state input, #route-state textarea');
        elements.navState = document.querySelector('#nav-state input, #nav-state textarea');
        elements.authNavState = document.querySelector('#auth-nav-state input, #auth-nav-state textarea');
        elements.navGroup = document.querySelector('.nav-group');
        elements.navButtons = elements.navGroup ? elements.navGroup.querySelectorAll('.nav-btn') : null;
    }

    function init() {
        if (initialized) return;
        
        cacheElements();
        
        // Wait for Gradio elements to be ready
        if (!elements.routeState || !elements.navState || !elements.authNavState) {
            setTimeout(init, 100);
            return;
        }
        
        // Set up event listeners on Gradio hidden inputs
        elements.routeState.addEventListener('input', onRouteStateChange);
        elements.navState.addEventListener('input', onNavStateChange);
        elements.authNavState.addEventListener('input', onAuthNavStateChange);
        
        // Browser back/forward
        window.addEventListener('popstate', handlePopState);
        
        // Sidebar clicks
        setupSidebarClicks();
        
        // Initial route resolution from current URL
        handlePopState();
        
        initialized = true;
        console.log('[Routing] Initialized successfully');
    }

    // Start initialization when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Re-initialize on Gradio re-renders (e.g., after auth)
    const observer = new MutationObserver(() => {
        if (initialized && !elements.routeState) {
            initialized = false;
            init();
        }
    });
    observer.observe(document.body, { childList: true, subtree: true });

})();
</script>
"""


# =============================================================================
# APP CREATION
# =============================================================================

def create_app():
    with gr.Blocks(
        title="Surface Crack Detection",
        fill_height=True,
    ) as app:

        # =====================================================================
        # STATE MANAGEMENT
        # =====================================================================
        
        # Single unified routing state - the source of truth for URL
        route_state = gr.Textbox(value="/", visible=False, elem_id="route-state")
        
        # Auth & user state
        auth_token = gr.State(None)
        user_info = gr.State({})
        prediction_history = gr.State([])

        # OAuth cleanup handled via launch
        gr.HTML("<!-- OAuth cleanup handled via launch -->")

        # =====================================================================
        # UI COMPONENTS
        # =====================================================================
        
        # Auth section (visible initially)
        auth = build_auth_section()
        
        # App section (hidden initially, shown after login)
        with gr.Column(elem_classes="app-container", visible=False) as app_section:
            with gr.Row(equal_height=False):
                sidebar = build_sidebar()
                with gr.Column(scale=4, elem_classes="content-area"):
                    dashboard = build_dashboard_page()
                    predict = build_predict_page()
                    user = build_user_page()
                    about = build_about_page()

        # Logout confirmation modal
        logout = build_logout_modal()

        # =====================================================================
        # AUTH NAVIGATION EVENTS
        # =====================================================================
        
        nav_auth_outputs = [
            auth["landing_col"], auth["login_col"], 
            auth["register_col"], auth["forgotpwd_col"]
        ]

        # Auth navigation buttons -> update auth_nav_state + route_state
        auth["go_login_btn"].click(
            fn=lambda: ("login", "/login"),
            outputs=[auth["auth_nav_state"], route_state]
        )
        auth["back_to_login_btn"].click(
            fn=lambda: ("login", "/login"),
            outputs=[auth["auth_nav_state"], route_state]
        )
        auth["back_to_login2_btn"].click(
            fn=lambda: ("login", "/login"),
            outputs=[auth["auth_nav_state"], route_state]
        )
        auth["show_forgot_btn"].click(
            fn=lambda: ("forgot", "/forgot"),
            outputs=[auth["auth_nav_state"], route_state]
        )
        auth["show_register_from_login_btn"].click(
            fn=lambda: ("register", "/register"),
            outputs=[auth["auth_nav_state"], route_state]
        )

        # Auth nav state change -> update visibility
        auth["auth_nav_state"].change(
            fn=auth_navigate,
            inputs=[auth["auth_nav_state"]],
            outputs=nav_auth_outputs + [auth["auth_nav_state"], route_state],
        )

        # =====================================================================
        # LOGIN FLOW
        # =====================================================================
        
        auth["login_btn"].click(
            fn=handle_login,
            inputs=[auth["login_email"], auth["login_password"]],
            outputs=[auth["login_error"], auth_token, user_info],
        ).then(
            fn=after_login_success,
            inputs=[auth_token, user_info],
            outputs=[auth["section"], app_section],
        ).then(
            fn=lambda u: (lambda n=u.get("full_name","User"), e=u.get("email",""): (
                f'<div style="display:flex;align-items:center;gap:0.6rem;">'
                f'<div class="sidebar-user-avatar">{n[0].upper() if n else "U"}</div>'
                f'<div><div class="sidebar-user-name">{n}</div>'
                f'<div class="sidebar-user-email">{e}</div></div></div>'
            ))(),
            inputs=[user_info],
            outputs=[sidebar["user_sidebar_info"]],
        ).then(
            fn=lambda h: _refresh_dashboard(h),
            inputs=[prediction_history],
            outputs=[dashboard["stats"], dashboard["recent"], dashboard["chart"], dashboard["severity"]],
        ).then(
            fn=lambda: ("Dashboard", "/dashboard"),
            outputs=[sidebar["nav_state"], route_state],
        )

        # =====================================================================
        # REGISTER & FORGOT PASSWORD
        # =====================================================================
        
        auth["register_btn"].click(
            fn=handle_register,
            inputs=[auth["reg_name"], auth["reg_email"], auth["reg_phone"], 
                    auth["reg_password"], auth["reg_confirm"]],
            outputs=[auth["register_msg"]],
        )

        auth["send_reset_btn"].click(
            fn=handle_forgot,
            inputs=[auth["forgot_email"]],
            outputs=[auth["forgot_msg"]],
        )

        # =====================================================================
        # GITHUB OAUTH
        # =====================================================================
        
        app.load(fn=check_oauth, outputs=[auth_token, user_info, auth["section"], app_section])
        app.load(fn=gen_github_link, outputs=[auth["github_link"]])

        # =====================================================================
        # MAIN APP NAVIGATION
        # =====================================================================
        
        # Sidebar nav_state change -> navigate pages
        sidebar["nav_state"].change(
            fn=navigate,
            inputs=[sidebar["nav_state"], user_info],
            outputs=[
                dashboard["page"], predict["page"], user["page"], about["page"],
                logout["modal"], sidebar["user_sidebar_info"], 
                sidebar["nav_state"], route_state
            ],
        )

        # =====================================================================
        # DEEP LINKING / BROWSER BACK-FORWARD SUPPORT
        # =====================================================================
        
        # When route_state changes (from JS popstate or direct navigation),
        # resolve the complete UI state
        route_state.change(
            fn=resolve_route_state,
            inputs=[route_state, user_info],
            outputs=[
                auth["section"], app_section,
                auth["landing_col"], auth["login_col"], auth["register_col"], auth["forgotpwd_col"],
                dashboard["page"], predict["page"], user["page"], about["page"],
                logout["modal"],
                sidebar["user_sidebar_info"],
                sidebar["nav_state"], auth["auth_nav_state"],
                route_state,
            ],
        )

        # =====================================================================
        # DASHBOARD PREDICTION
        # =====================================================================
        
        dashboard["run"].click(
            fn=run_dash_prediction,
            inputs=[dashboard["upload"], prediction_history],
            outputs=[prediction_history, dashboard["stats"], dashboard["recent"], 
                     dashboard["chart"], dashboard["severity"]],
        )

        # =====================================================================
        # PREDICT PAGE
        # =====================================================================
        
        predict["run"].click(
            fn=run_predict_prediction,
            inputs=[predict["upload"], predict["class_selector"], prediction_history],
            outputs=[predict["results"], predict["report"]],
        )

        # =====================================================================
        # USER PAGE REFRESH
        # =====================================================================
        
        sidebar["nav_state"].change(
            fn=refresh_user,
            inputs=[user_info, prediction_history],
            outputs=[user["stats"], user["profile"], user["activity"]],
        )

        # =====================================================================
        # LOGOUT FLOW
        # =====================================================================
        
        logout["cancel_btn"].click(
            fn=cancel_logout,
            outputs=[
                dashboard["page"], predict["page"], user["page"], about["page"],
                logout["modal"], sidebar["nav_state"], route_state
            ],
        )

        logout["confirm_btn"].click(
            fn=do_logout,
            outputs=[
                auth_token, user_info, app_section, auth["section"],
                auth["landing_col"], auth["login_col"], auth["register_col"], auth["forgotpwd_col"],
                sidebar["nav_state"], route_state
            ],
        )

    return app, CUSTOM_CSS, NAV_JS
