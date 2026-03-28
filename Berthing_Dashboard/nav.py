import streamlit as st
from streamlit.errors import StreamlitAPIException


def _safe_switch(page: str):
    try:
        st.switch_page(page)
    except StreamlitAPIException:
        st.warning("Bu sayfa mevcut çalışma modunda açılamadı. Uygulamayı `Home.py` üzerinden başlatın.")


def render_top_nav(active_page: str):
    st.markdown(
        """
        <style>
        [data-testid="stButton"] > button[kind="secondary"] {
            background: #0a0f14 !important;
            color: #cce8f4 !important;
            border: 1px solid #1b2731 !important;
            box-shadow: none !important;
        }
        [data-testid="stButton"] > button[kind="secondary"]:hover {
            background: #111821 !important;
            border-color: #2a3b49 !important;
        }
        [data-testid="stButton"] > button[kind="secondary"]:disabled {
            background: #0a0f14 !important;
            color: #6d7c88 !important;
            border: 1px solid #1b2731 !important;
            box-shadow: none !important;
            cursor: not-allowed !important;
            opacity: 1 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Hakkımızda", use_container_width=True, disabled=(active_page == "about")):
            _safe_switch("pages/2_Hakkimizda.py")

    with col2:
        if st.button("Ana Sayfa", use_container_width=True, disabled=(active_page == "home")):
            _safe_switch("Home.py")

    with col3:
        if st.button("Simülasyon", use_container_width=True, disabled=(active_page == "simulation")):
            _safe_switch("pages/1_Simulasyon.py")
