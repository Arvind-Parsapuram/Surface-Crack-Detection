import os

CLASSES = ["Potholes", "Cracks", "Patch", "Surface Defects"]
SEVERITY_ORDER = ["Low", "Medium", "High", "Critical"]
SEVERITY_COLOR = {
    "Low": "#2ecc71",
    "Medium": "#f39c12",
    "High": "#e74c3c",
    "Critical": "#8b0000",
    "---": "#b0b0b0",
}
ACCENT = "#6C5CE7"
ACCENT_LIGHT = "#8B7CF7"
ACCENT_DARK = "#4A3DB8"

APP_URL = os.getenv("APP_URL", "https://amruthjakku-surface-crack-detection.hf.space/login")

ICONS = {
    "dashboard": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>',
    "predict": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>',
    "user": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/></svg>',
    "about": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>',
    "logout": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>',
    "upload": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>',
    "chart": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
    "check": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>',
    "warning": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    "target": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
    "image": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>',
    "clock": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
    "mail": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>',
    "lock": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>',
    "phone": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>',
    "arrow-left": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>',
    "download": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>',
    "github": '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z"/></svg>',
    "star": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>',
    "road": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 22L12 2l10 20H2z"/><line x1="12" y1="10" x2="12" y2="16"/><line x1="8" y1="16" x2="16" y2="16"/></svg>',
}

CUSTOM_CSS = """
:root {
    --accent: #6C5CE7;
    --accent-light: #8B7CF7;
    --accent-dark: #4A3DB8;
    --accent-glow: rgba(108, 92, 231, 0.12);
    --sidebar-bg: #0F1117;
    --sidebar-hover: #1E2130;
    --sidebar-active: #252840;
    --sidebar-text: #7A7A9E;
    --sidebar-text-active: #FFFFFF;
    --surface: #F0F2F8;
    --bg-card: #FFFFFF;
    --bg-card-alt: #F8F9FE;
    --text-primary: #1A1A2E;
    --text-secondary: #7A7A9E;
    --text-muted: #B0B0C8;
    --border-light: #E8EAF0;
    --input-bg: #FFFFFF;
    --input-border: #D0D0E0;
    --shadow-color: rgba(0,0,0,0.06);
    --shadow-sm: 0 1px 3px rgba(0,0,0,0.04);
    --shadow-md: 0 4px 16px rgba(0,0,0,0.06);
    --shadow-lg: 0 8px 32px rgba(0,0,0,0.1);
    --radius: 12px;
    --radius-lg: 16px;
    --transition: 0.2s;
    --nav-icon-color: #6A6A8E;
}
@media (prefers-color-scheme: dark) {
    :root {
        --surface: #0E1017;
        --bg-card: #1A1D27;
        --bg-card-alt: #1E2130;
        --text-primary: #E8E8F0;
        --text-secondary: #9A9AB5;
        --text-muted: #6A6A85;
        --border-light: #2A2D3A;
        --input-bg: #1A1D27;
        --input-border: #2A2D3A;
        --shadow-color: rgba(0,0,0,0.3);
        --shadow-sm: 0 1px 3px rgba(0,0,0,0.2);
        --shadow-md: 0 4px 16px rgba(0,0,0,0.25);
        --shadow-lg: 0 8px 32px rgba(0,0,0,0.35);
        --accent-glow: rgba(108, 92, 231, 0.2);
        --sidebar-bg: #0A0C12;
        --sidebar-hover: #151822;
        --sidebar-active: #1C1F2E;
        --sidebar-text: #6A6A8E;
        --nav-icon-color: #7A7A9E;
    }
}

.gradio-container { font-family: 'Inter', -apple-system, sans-serif !important; background: var(--surface) !important; }
footer, .gr-footer { display: none !important; }

/* ---- Input overrides ---- */
input, textarea, select { background: var(--input-bg) !important; border-color: var(--input-border) !important; color: var(--text-primary) !important; border-radius: 8px !important; }
input:focus, textarea:focus { border-color: var(--accent) !important; box-shadow: 0 0 0 3px var(--accent-glow) !important; }
.gr-box { border-color: var(--border-light) !important; }

/* ---- Auth ---- */
.auth-container {
    min-height: 100vh;
    background: radial-gradient(circle at 50% 50%, rgba(108, 92, 231, 0.18), transparent 65%), 
                linear-gradient(-45deg, #09071a, #0f0f1f, #0d162a, #0b203c);
    background-size: 400% 400%;
    animation: gradientShift 15s ease infinite;
    display: flex !important;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    position: relative;
    overflow: hidden;
}
.auth-container::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image: 
        linear-gradient(rgba(108, 92, 231, 0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(108, 92, 231, 0.04) 1px, transparent 1px);
    background-size: 45px 45px;
    background-position: center;
    mask-image: radial-gradient(circle at center, black 40%, transparent 80%);
    -webkit-mask-image: radial-gradient(circle at center, black 40%, transparent 80%);
    pointer-events: none;
}
@keyframes gradientShift { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }

.auth-box {
    --bg-card: rgba(15, 18, 36, 0.72);
    --text-primary: #FFFFFF;
    --text-secondary: rgba(255, 255, 255, 0.6);
    --text-muted: rgba(255, 255, 255, 0.4);
    --border-light: rgba(255, 255, 255, 0.08);
    --input-bg: rgba(255, 255, 255, 0.04);
    --input-border: rgba(255, 255, 255, 0.1);
    
    /* Gradio inner overrides */
    --block-background-fill: transparent !important;
    --block-border-width: 0px !important;
    --block-label-text-color: rgba(255, 255, 255, 0.85) !important;
    --block-title-text-color: #FFFFFF !important;
    --body-text-color: #FFFFFF !important;
    
    background: var(--bg-card) !important;
    backdrop-filter: blur(24px) saturate(180%);
    -webkit-backdrop-filter: blur(24px) saturate(180%);
    border: 1px solid var(--border-light) !important;
    border-radius: var(--radius-lg);
    padding: 2.5rem 2rem;
    width: 100%;
    max-width: 420px;
    box-shadow: 0 24px 60px rgba(0, 0, 0, 0.55), inset 0 1px 1px rgba(255, 255, 255, 0.12);
    animation: slideUpFade 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    z-index: 10;
}
@keyframes slideUpFade { from { opacity: 0; transform: translateY(24px); } to { opacity: 1; transform: translateY(0); } }

.auth-logo {
    display: flex !important;
    align-items: center;
    justify-content: center;
    width: 56px;
    height: 56px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    margin: 0 auto 1rem !important;
    box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1);
}
.auth-logo svg {
    width: 24px;
    height: 24px;
    color: #a78bfa;
    filter: drop-shadow(0 0 6px rgba(167, 139, 250, 0.4));
}
.auth-title { text-align: center; font-size: 1.5rem; font-weight: 700; color: #FFFFFF !important; margin-bottom: 0.25rem; }
.auth-subtitle { text-align: center; color: rgba(255, 255, 255, 0.5) !important; font-size: 0.88rem; margin-bottom: 1.5rem; }

.auth-box .auth-error {
    background: rgba(239, 68, 68, 0.1) !important;
    color: #fca5a5 !important;
    border: 1px solid rgba(239, 68, 68, 0.25) !important;
    padding: 0.6rem 1rem;
    border-radius: 8px;
    font-size: 0.85rem;
    margin-bottom: 1rem;
    text-align: center;
    animation: shake 0.3s ease;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    justify-content: center;
}
.auth-box .auth-success {
    background: rgba(16, 185, 129, 0.1) !important;
    color: #6ee7b7 !important;
    border: 1px solid rgba(16, 185, 129, 0.25) !important;
    padding: 0.6rem 1rem;
    border-radius: 8px;
    font-size: 0.85rem;
    margin-bottom: 1rem;
    text-align: center;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    justify-content: center;
}
@keyframes shake { 0%,100% { transform: translateX(0); } 25% { transform: translateX(-4px); } 75% { transform: translateX(4px); } }

.auth-box .auth-divider { display: flex; align-items: center; gap: 1rem; margin: 1rem 0; color: rgba(255, 255, 255, 0.4) !important; font-size: 0.8rem; }
.auth-box .auth-divider::before, .auth-box .auth-divider::after { content: ''; flex: 1; border-top: 1px solid rgba(255, 255, 255, 0.1) !important; }

.auth-box label,
.auth-box label span {
    color: rgba(255, 255, 255, 0.85) !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    margin-bottom: 0.25rem !important;
}

.auth-box input[type="text"],
.auth-box input[type="password"],
.auth-box input, 
.auth-box textarea, 
.auth-box select { 
    background: rgba(255, 255, 255, 0.04) !important; 
    border: 1px solid rgba(255, 255, 255, 0.1) !important; 
    color: #FFFFFF !important; 
    border-radius: 8px !important;
    height: 42px !important;
    padding: 0.65rem 0.85rem !important;
    transition: all 0.2s ease !important;
}
.auth-box input::placeholder {
    color: rgba(255, 255, 255, 0.35) !important;
}
.auth-box input:focus, 
.auth-box textarea:focus { 
    border-color: #8b7cf7 !important; 
    box-shadow: 0 0 0 3px rgba(139, 124, 247, 0.25) !important; 
    background: rgba(255, 255, 255, 0.07) !important;
}

/* Primary Form Action Buttons */
.auth-box button:not(.auth-link-btn):not(.auth-link-btn button) {
    background: linear-gradient(135deg, #6C5CE7, #8B7CF7) !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    padding: 0.75rem 1.5rem !important;
    box-shadow: 0 4px 15px rgba(108, 92, 231, 0.35) !important;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
    cursor: pointer !important;
    width: 100% !important;
}
.auth-box button:not(.auth-link-btn):not(.auth-link-btn button):hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(108, 92, 231, 0.55) !important;
    filter: brightness(1.1) !important;
}
.auth-box button:not(.auth-link-btn):not(.auth-link-btn button):active {
    transform: translateY(0) !important;
}

.auth-link-btn, .auth-link-btn button { background: none !important; border: none !important; color: rgba(255, 255, 255, 0.55) !important; font-size: 0.82rem !important; cursor: pointer; padding: 0.5rem !important; transition: color var(--transition) !important; box-shadow: none !important; }
.auth-link-btn:hover, .auth-link-btn:hover button { color: #8b7cf7 !important; background: none !important; text-decoration: underline !important; }

/* Landing hero */
.landing-hero { text-align: center; padding: 1rem 0.5rem; }
.landing-road-icon {
    display: inline-flex !important;
    align-items: center;
    justify-content: center;
    width: 64px;
    height: 64px;
    background: linear-gradient(135deg, rgba(108, 92, 231, 0.2), rgba(139, 124, 247, 0.2));
    border: 1px solid rgba(139, 124, 247, 0.3);
    border-radius: 20px;
    margin: 0 auto 1.5rem !important;
    box-shadow: 0 8px 24px rgba(108, 92, 231, 0.25), inset 0 1px 1px rgba(255,255,255,0.2);
    animation: float 4s ease-in-out infinite;
}
.landing-road-icon svg {
    width: 32px !important;
    height: 32px !important;
    color: #a78bfa;
    filter: drop-shadow(0 0 8px rgba(167,139,250,0.5));
}
@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-6px); }
}
.landing-title {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #FFFFFF 30%, #a78bfa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.75rem;
    line-height: 1.2;
    letter-spacing: -0.02em;
}
.landing-desc {
    font-size: 0.95rem;
    color: rgba(255,255,255,0.7);
    max-width: 360px;
    margin: 0 auto 1.75rem;
    line-height: 1.6;
}
.landing-features { display: flex; gap: 0.5rem; justify-content: center; flex-wrap: wrap; margin-bottom: 2rem; }
.landing-feat-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 0.4rem 0.8rem;
    border-radius: 99px;
    font-size: 0.75rem;
    color: rgba(255,255,255,0.85);
    transition: all 0.2s ease;
}
.landing-feat-chip:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.2);
    transform: translateY(-1px);
}
.landing-feat-chip svg { color: #a78bfa; width: 14px; height: 14px; }

/* GitHub link */
.auth-github-link a {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.65rem;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    background: rgba(255, 255, 255, 0.08) !important;
    color: white !important;
    text-decoration: none;
    font-size: 0.9rem;
    font-weight: 500;
    transition: all 0.2s;
}
.auth-github-link a:hover {
    background: rgba(255, 255, 255, 0.15) !important;
    border-color: rgba(255, 255, 255, 0.3) !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.25);
}

.sidebar { background: var(--sidebar-bg) !important; border-right: 1px solid var(--border-light); padding: 1.5rem 0 !important; }
.sidebar-inner { padding: 0 0.75rem; height: 100%; display: flex; flex-direction: column; }
.app-logo { display: flex; align-items: center; gap: 0.5rem; font-size: 0.95rem; font-weight: 700; color: var(--sidebar-text-active); padding: 0 0.5rem; margin-bottom: 0.15rem; }
.app-logo svg { color: var(--accent); }
.app-tagline { font-size: 0.7rem; color: var(--sidebar-text); padding: 0 0.5rem; margin-bottom: 1.5rem; }
.nav-group { display: flex; flex-direction: column; gap: 2px; }
.nav-btn { display: flex; align-items: center; gap: 0.6rem; width: 100%; padding: 0.6rem 0.75rem; border: none; border-radius: 8px; background: transparent; color: var(--sidebar-text); font-size: 0.85rem; cursor: pointer; transition: all 0.15s; text-align: left; border-left: 3px solid transparent; }
.nav-btn svg { flex-shrink: 0; color: var(--nav-icon-color); transition: color 0.15s; }
.nav-btn:hover { background: var(--sidebar-hover); color: #ccc; }
.nav-btn:hover svg { color: #aaa; }
.nav-btn.active { background: var(--sidebar-active); color: var(--sidebar-text-active); border-left-color: var(--accent); font-weight: 600; }
.nav-btn.active svg { color: var(--accent); }
.nav-btn.nav-logout { margin-top: 0.5rem; }
.nav-btn.nav-logout svg { color: #ef4444; }
.sidebar-footer { margin-top: auto; padding: 1rem 0.75rem 0; border-top: 1px solid var(--border-light); }
.sidebar-user-avatar { width: 32px; height: 32px; border-radius: 50%; background: linear-gradient(135deg, var(--accent), var(--accent-light)); color: white; display: flex; align-items: center; justify-content: center; font-weight: 600; font-size: 0.85rem; flex-shrink: 0; }
.sidebar-user-name { font-size: 0.82rem; color: var(--sidebar-text-active); font-weight: 500; line-height: 1.2; }
.sidebar-user-email { font-size: 0.7rem; color: var(--sidebar-text); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 130px; }

.app-container { background: var(--surface); }
.content-area { padding: 1.5rem 2rem; }
@keyframes pageIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }

.card { background: var(--bg-card); border: 1px solid var(--border-light); border-radius: var(--radius-lg); padding: 1.25rem 1.5rem; box-shadow: var(--shadow-sm); margin-bottom: 1rem; transition: transform var(--transition), box-shadow var(--transition); }
.card:hover { box-shadow: var(--shadow-md); }
.card-highlight { border-left: 3px solid var(--accent); }
.card-header { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem; }
.card-header svg { flex-shrink: 0; color: var(--accent); }
.card-title { font-size: 1rem; font-weight: 600; color: var(--text-primary); }
.card-desc { font-size: 0.82rem; color: var(--text-secondary); line-height: 1.5; }

.stat-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 1.5rem; }
.stat-card { background: var(--bg-card); border: 1px solid var(--border-light); border-radius: var(--radius-lg); padding: 1.25rem 0.75rem; box-shadow: var(--shadow-sm); text-align: center; transition: all var(--transition); position: relative; overflow: hidden; }
.stat-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; border-radius: 16px 16px 0 0; }
.stat-card:hover { transform: translateY(-2px); box-shadow: var(--shadow-md); }
.stat-icon-wrap { display: inline-flex; align-items: center; justify-content: center; width: 40px; height: 40px; border-radius: 10px; margin-bottom: 0.5rem; }
.stat-icon-wrap svg { width: 20px; height: 20px; }
.stat-value { font-size: 1.5rem; font-weight: 700; color: var(--text-primary); line-height: 1.2; }
.stat-label { font-size: 0.75rem; color: var(--text-secondary); margin-top: 2px; }

.page-title { font-size: 1.4rem; font-weight: 700; color: var(--text-primary); margin-bottom: 0.15rem; }
.page-sub { color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 1.25rem; }
.pill { display: inline-block; padding: 3px 12px; border-radius: 999px; font-size: 0.75rem; font-weight: 600; color: white; }

.upload-zone { border: 2px dashed var(--border-light); border-radius: var(--radius); padding: 2rem 1rem; text-align: center; transition: all var(--transition); cursor: pointer; }
.upload-zone:hover { border-color: var(--accent); background: var(--accent-glow); }
.upload-zone-icon { display: flex; justify-content: center; margin-bottom: 0.5rem; }
.upload-zone-icon svg { width: 36px; height: 36px; color: var(--text-muted); }
.upload-zone-text { font-size: 0.85rem; color: var(--text-secondary); }
.upload-zone-sub { font-size: 0.72rem; color: var(--text-muted); margin-top: 4px; }

.progress-track { background: var(--border-light); border-radius: 999px; height: 20px; overflow: hidden; margin-bottom: 6px; }
.progress-fill { height: 100%; border-radius: 999px; transition: width 0.4s ease; background: var(--accent); }
.progress-label { font-size: 0.78rem; display: flex; justify-content: space-between; margin-bottom: 2px; color: var(--text-primary); }

.feature-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin: 1rem 0; }
.feat-card { background: var(--bg-card-alt); border-radius: var(--radius); padding: 1rem; text-align: center; }
.feat-card svg { width: 24px; height: 24px; color: var(--accent); margin-bottom: 0.4rem; }
.feat-card .ft { font-weight: 600; font-size: 0.85rem; color: var(--text-primary); }
.feat-card .fd { font-size: 0.75rem; color: var(--text-secondary); margin-top: 2px; }

.team-row { display: flex; gap: 1rem; align-items: center; padding: 0.75rem 0; border-bottom: 1px solid var(--border-light); }
.team-row:last-child { border-bottom: none; }
.team-av { width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 600; font-size: 0.9rem; color: white; flex-shrink: 0; }

.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.45); backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; z-index: 9999; animation: fadeIn 0.2s ease; }
.modal-box { background: var(--bg-card); border: 1px solid var(--border-light); border-radius: var(--radius-lg); padding: 2rem; max-width: 380px; width: 90%; text-align: center; box-shadow: var(--shadow-lg); animation: scaleUp 0.25s ease; }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes scaleUp { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }

.act-item { display: flex; gap: 0.75rem; align-items: center; padding: 0.6rem 0; border-bottom: 1px solid var(--border-light); }
.act-item:last-child { border-bottom: none; }
.act-thumb { width: 48px; height: 48px; border-radius: 8px; object-fit: cover; flex-shrink: 0; border: 1px solid var(--border-light); }
.act-info { flex: 1; min-width: 0; }
.act-class { font-weight: 600; font-size: 0.85rem; color: var(--text-primary); }
.act-meta { font-size: 0.75rem; color: var(--text-secondary); }
.act-time { font-size: 0.72rem; color: var(--text-muted); flex-shrink: 0; }
.severity-badge { display: inline-flex; align-items: center; gap: 0.35rem; padding: 4px 12px; border-radius: 999px; font-size: 0.8rem; font-weight: 600; }
.tech-badge { display: inline-flex; align-items: center; gap: 0.35rem; background: var(--bg-card-alt); border: 1px solid var(--border-light); padding: 0.3rem 0.65rem; border-radius: 6px; font-size: 0.72rem; color: var(--text-secondary); margin: 0.15rem; }
.tech-badge svg { width: 14px; height: 14px; color: var(--accent); }
.dl-btn { display: inline-flex; align-items: center; gap: 0.4rem; padding: 0.5rem 1.2rem; background: var(--accent); color: white; border-radius: 8px; text-decoration: none; font-size: 0.85rem; font-weight: 500; transition: all 0.2s; border: none; cursor: pointer; }
.dl-btn:hover { background: var(--accent-dark); transform: translateY(-1px); box-shadow: 0 4px 12px var(--accent-glow); }
"""
