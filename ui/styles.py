"""Custom CSS for the CleanTrace command desk."""

import streamlit as st


def load_css() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap');

        :root {
            --primary: #34d399;
            --primary-dark: #059669;
            --accent: #5eead4;
            --gold: #fbbf24;
            --bg: #071412;
            --bg-2: #0c2420;
            --card: rgba(14, 42, 38, 0.82);
            --text: #ecfdf5;
            --muted: #9cb8b0;
            --border: rgba(52, 211, 153, 0.22);
            --danger: #fb7185;
            --warning: #fbbf24;
            --success: #34d399;
        }

        html, body, [data-testid="stAppViewContainer"], .stApp {
            background:
                radial-gradient(1200px 500px at 12% -10%, rgba(16, 185, 129, 0.22), transparent 55%),
                radial-gradient(900px 400px at 100% 0%, rgba(14, 165, 233, 0.16), transparent 50%),
                linear-gradient(165deg, #071412 0%, #0a1f1c 48%, #08201c 100%) !important;
            color: var(--text) !important;
            font-family: "IBM Plex Sans", sans-serif;
        }

        [data-testid="stHeader"] {
            background: transparent !important;
        }

        #MainMenu, footer { visibility: hidden; }
        .stAppDeployButton, [data-testid="stToolbar"] { display: none !important; }
        [data-testid="stFileUploaderDropzone"] {
            background: rgba(6, 24, 21, 0.72) !important;
            border: 1px dashed var(--border) !important;
            color: var(--text) !important;
        }

        h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            font-family: "Space Grotesk", sans-serif !important;
            color: var(--text) !important;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0b1f1c 0%, #071412 100%) !important;
            border-right: 1px solid var(--border);
        }

        [data-testid="stSidebar"] * {
            color: var(--text);
        }

        .hero {
            background: linear-gradient(135deg, rgba(16,185,129,0.18), rgba(8,47,73,0.35));
            border: 1px solid var(--border);
            border-radius: 22px;
            padding: 1.4rem 1.7rem 1.2rem;
            margin: 0.2rem 0 1.4rem 0;
            box-shadow: 0 18px 50px rgba(0,0,0,0.28);
            position: relative;
            overflow: hidden;
        }
        .hero::after {
            content: "";
            position: absolute;
            right: -40px;
            top: -40px;
            width: 180px;
            height: 180px;
            background: radial-gradient(circle, rgba(52,211,153,0.35), transparent 70%);
        }
        .hero-kicker {
            font-size: 0.72rem;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            color: var(--accent);
            font-weight: 600;
            margin-bottom: 0.35rem;
        }
        .hero-title {
            font-family: "Space Grotesk", sans-serif;
            font-size: 2.35rem;
            font-weight: 700;
            letter-spacing: -0.03em;
            line-height: 1.1;
            margin: 0;
        }
        .hero-title span { color: var(--primary); }
        .hero-sub {
            color: var(--muted);
            margin-top: 0.45rem;
            font-size: 1.02rem;
            max-width: 52rem;
        }
        .pipeline {
            display: flex;
            flex-wrap: wrap;
            gap: 0.55rem;
            margin-top: 1rem;
        }
        .pipe {
            background: rgba(6, 24, 21, 0.7);
            border: 1px solid var(--border);
            color: var(--accent);
            border-radius: 999px;
            padding: 0.28rem 0.8rem;
            font-size: 0.78rem;
            font-weight: 600;
            letter-spacing: 0.02em;
        }

        .brand {
            font-family: "Space Grotesk", sans-serif;
            font-size: 1.45rem;
            font-weight: 700;
            letter-spacing: -0.03em;
            color: var(--primary);
            margin-bottom: 0.15rem;
        }
        .subbrand {
            font-size: 0.82rem;
            color: var(--muted);
            margin-bottom: 1.15rem;
            font-weight: 500;
        }

        .alert {
            background: rgba(251, 113, 133, 0.12);
            border: 1px solid rgba(251, 113, 133, 0.4);
            color: #fecdd3;
            border-radius: 12px;
            padding: 1.1rem 1.3rem;
            margin: 1.2rem 0;
        }
        .notice {
            background: rgba(6, 24, 21, 0.7);
            border: 1px dashed var(--border);
            border-radius: 12px;
            padding: 1.2rem;
            margin: 1rem 0;
            color: #d1fae5;
            font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
            white-space: pre-wrap;
            font-size: 0.88rem;
            line-height: 1.7;
        }
        .status-row {
            display: flex;
            align-items: center;
            gap: 0.7rem;
            margin: 0.45rem 0;
            font-size: 0.9rem;
        }
        .dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
        .dot-on { background: var(--success); box-shadow: 0 0 0 4px rgba(52,211,153,0.22); }
        .dot-off { background: #334155; }
        .badge {
            display: inline-block;
            padding: 0.15rem 0.55rem;
            border-radius: 999px;
            font-size: 0.68rem;
            font-weight: 700;
            letter-spacing: 0.06em;
        }
        .badge-ok { background: rgba(52,211,153,0.18); color: #6ee7b7; border: 1px solid rgba(52,211,153,0.4); }
        .badge-off { background: rgba(148,163,184,0.12); color: #94a3b8; border: 1px solid rgba(148,163,184,0.25); }

        .log-entry {
            padding: 0.8rem 1rem;
            border-bottom: 1px solid var(--border);
            font-size: 0.85rem;
            font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
            color: var(--muted);
            background: rgba(6,24,21,0.45);
        }
        .log-entry b { color: var(--text); }
        .tag-sentinel { color: #38bdf8; }
        .tag-civic { color: #c4b5fd; }
        .tag-resolver { color: var(--accent); }

        .stButton > button {
            background: linear-gradient(180deg, #34d399, #059669) !important;
            color: #042f2e !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.65rem 1.25rem !important;
            font-weight: 700 !important;
        }
        .stButton > button:hover {
            box-shadow: 0 8px 22px rgba(16,185,129,0.35) !important;
        }

        div[data-testid="stMetric"] {
            background: rgba(14, 42, 38, 0.7);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 0.85rem 0.9rem;
        }
        div[data-testid="stMetric"] label { color: var(--muted) !important; }
        div[data-testid="stMetric"] [data-testid="stMetricValue"] { color: var(--text) !important; }

        [data-testid="stTabs"] button { color: var(--muted); }
        [data-testid="stTabs"] button[aria-selected="true"] {
            color: var(--primary) !important;
        }

        .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
            background: rgba(6, 24, 21, 0.75) !important;
            color: var(--text) !important;
            border-radius: 10px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
