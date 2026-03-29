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
        .github-cta-wrap {
            display: flex;
            justify-content: flex-end;
            margin-top: 6px;
            margin-bottom: 6px;
        }
        .github-cta {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 12px;
            border: 1px solid #0d2d40;
            border-radius: 8px;
            background: #0a0f14;
            color: #cce8f4 !important;
            text-decoration: none !important;
            font-size: 0.85rem;
            font-weight: 600;
        }
        .github-cta:hover {
            border-color: #00e5ff;
            box-shadow: 0 0 10px rgba(0, 229, 255, 0.35);
        }
        .github-cta img {
            width: 18px;
            height: 18px;
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

    st.markdown(
        """
        <div class="github-cta-wrap">
          <a class="github-cta" href="https://github.com/EyupEfeAslan2/GallipoliSpaceStation" target="_blank">
            <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="GitHub" />
            Proje GitHub Reposu
          </a>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_simulation_subnav(active_sim_page: str):
    st.markdown(
        """
        <style>
        .sim-subnav-note {
            font-family: 'Share Tech Mono', monospace;
            color: #8daabf;
            font-size: 0.74rem;
            letter-spacing: 1px;
            margin-top: 2px;
            margin-bottom: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    s1, s2, s3 = st.columns(3)

    with s1:
        if st.button("Berthing Simülasyonu", use_container_width=True, disabled=(active_sim_page == "berthing")):
            _safe_switch("pages/1_Simulasyon.py")

    with s2:
        if st.button("Otonom Mekanizma", use_container_width=True, disabled=(active_sim_page == "otonom")):
            _safe_switch("pages/3_Otonom_Mekanizma.py")

    with s3:
        if st.button("Savunma Mekanizması", use_container_width=True, disabled=(active_sim_page == "savunma")):
            _safe_switch("pages/4_Savunma_Mekanizmasi.py")

    st.markdown(
        '<div class="sim-subnav-note">Simülasyon Alt Sayfaları: Berthing, Otonom Mekanizma, Savunma Mekanizması</div>',
        unsafe_allow_html=True,
    )
