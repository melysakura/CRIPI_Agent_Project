"""Custom page styling for a wider, professional development-cooperation look."""

import streamlit as st

from components.theme import BORDER_BLUE, CARD_BLUE, CHART_BLUE, DARK_BLUE, PAGE_BG


def apply_page_style() -> None:
    """Inject CSS to widen the layout and style the dashboard background."""
    st.markdown(
        f"""
        <style>
            .block-container {{
                max-width: 96%;
                padding-top: 1.5rem;
                padding-bottom: 2rem;
            }}

            .stApp {{
                background: {PAGE_BG};
            }}

            h1, .page-title {{
                color: {DARK_BLUE} !important;
                text-align: center;
            }}

            h2, h3, h4, label {{
                color: {DARK_BLUE} !important;
            }}

            h2, [data-testid="stHeader"] {{
                font-size: 1.65rem !important;
            }}

            .page-caption {{
                color: {DARK_BLUE} !important;
                text-align: center;
                margin-bottom: 1.5rem;
            }}

            .kpi-card {{
                background: {CARD_BLUE};
                border: 2px solid {BORDER_BLUE};
                border-radius: 12px;
                padding: 1rem 1.1rem;
                box-shadow: 0 2px 6px rgba(26, 54, 93, 0.12);
                min-height: 130px;
            }}

            .kpi-card-split {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 0.75rem;
            }}

            .kpi-card-left {{
                flex: 1;
            }}

            .kpi-label {{
                color: {DARK_BLUE};
                font-size: 0.95rem;
                font-weight: 600;
                margin-bottom: 0.35rem;
            }}

            .kpi-state-large {{
                color: {DARK_BLUE};
                font-size: 1.3rem;
                font-weight: 700;
                line-height: 1.2;
            }}

            .kpi-value {{
                color: {DARK_BLUE};
                font-size: 2rem;
                font-weight: 700;
                line-height: 1.1;
            }}

            .kpi-value-right {{
                color: {DARK_BLUE};
                font-size: 2rem;
                font-weight: 700;
                text-align: right;
                white-space: nowrap;
            }}

            .kpi-value-highlight-high {{
                color: #C0392B;
                font-size: 2.3rem;
                font-weight: 700;
                text-align: right;
                white-space: nowrap;
            }}

            .kpi-value-highlight-low {{
                color: #27AE60;
                font-size: 2.3rem;
                font-weight: 700;
                text-align: right;
                white-space: nowrap;
            }}

            .state-profile-title {{
                font-size: 1.45rem;
                font-weight: 700;
                color: {DARK_BLUE};
                margin: 0.75rem 0 1rem 0;
                text-align: center;
            }}

            .dimension-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 1rem;
                max-width: 1100px;
                margin: 0 auto;
            }}

            .dimension-cell {{
                background: {CARD_BLUE};
                border: 2px solid {BORDER_BLUE};
                border-radius: 10px;
                padding: 0.85rem 1rem;
            }}

            .dimension-name {{
                font-size: 1.1rem;
                font-weight: 700;
                color: {DARK_BLUE};
                margin-bottom: 0.2rem;
            }}

            .dimension-score {{
                font-size: 1.9rem;
                font-weight: 700;
                color: {DARK_BLUE};
                margin-bottom: 0.55rem;
            }}

            .indicator-line {{
                font-size: 0.95rem;
                color: {DARK_BLUE};
                margin: 0.18rem 0;
                line-height: 1.4;
            }}

            .indicator-value {{
                font-weight: 700;
                color: {DARK_BLUE};
            }}

            .indicator-unit {{
                color: {DARK_BLUE};
                opacity: 0.85;
                font-size: 0.88rem;
            }}

            .profile-placeholder {{
                background: {CARD_BLUE};
                border: 2px solid {BORDER_BLUE};
                border-radius: 12px;
                padding: 1rem;
                text-align: center;
                color: {DARK_BLUE};
                margin-top: 0.75rem;
            }}

            .intro-panel {{
                background: {CARD_BLUE};
                border: 2px solid {BORDER_BLUE};
                border-radius: 12px;
                padding: 1rem 1.25rem;
                color: {DARK_BLUE};
                line-height: 1.55;
                margin-bottom: 1.25rem;
            }}

            .intro-panel ul {{
                margin: 0.5rem 0 0 1.2rem;
                padding: 0;
            }}

            .intro-panel li {{
                margin: 0.35rem 0;
            }}

            .delta-legend {{
                background: {CARD_BLUE};
                border: 2px solid {BORDER_BLUE};
                border-radius: 12px;
                padding: 0.9rem 1.15rem;
                color: {DARK_BLUE};
                line-height: 1.55;
                margin: 0.75rem 0 1.25rem 0;
            }}

            .cluster-summary-card {{
                background: {CARD_BLUE};
                border: 2px solid {BORDER_BLUE};
                border-radius: 12px;
                padding: 1rem 1.1rem;
                margin-bottom: 1rem;
            }}

            .cluster-summary-title {{
                font-size: 1.25rem;
                font-weight: 700;
                color: {DARK_BLUE};
                margin-bottom: 0.25rem;
            }}

            .cluster-summary-subtitle {{
                font-size: 0.95rem;
                color: {DARK_BLUE};
                margin-bottom: 0.75rem;
                opacity: 0.9;
            }}

            .cluster-member-list {{
                display: flex;
                flex-wrap: wrap;
                gap: 0.45rem;
            }}

            .cluster-chip {{
                display: inline-block;
                background: rgba(255, 255, 255, 0.55);
                border: 2px solid {BORDER_BLUE};
                border-radius: 999px;
                padding: 0.2rem 0.65rem;
                font-size: 0.85rem;
                color: {DARK_BLUE};
                font-weight: 600;
            }}

            .stCaption, [data-testid="stCaptionContainer"] {{
                color: {DARK_BLUE} !important;
            }}

            .stPlotlyChart, .stPlotlyChart > div {{
                background: {PAGE_BG} !important;
            }}

            iframe {{
                background: {PAGE_BG} !important;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
