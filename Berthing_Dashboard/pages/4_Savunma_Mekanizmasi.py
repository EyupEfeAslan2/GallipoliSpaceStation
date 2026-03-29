import streamlit as st
from pathlib import Path
from nav import render_top_nav, render_simulation_subnav

st.set_page_config(
    page_title="GALLIPOLI TUA HACKATHON | Savunma Mekanizması",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ASSETS_DIR = Path(__file__).resolve().parents[1] / "assets"
LAZER_VIDEO = ASSETS_DIR / "LazerVurus.mp4"
KACIS_VIDEO = ASSETS_DIR / "Kacis2.mp4"

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@500;700&display=swap');

:root {
    --bg-dark: #040b14;
    --cyan: #00e5ff;
    --card-bg: #0b1f30;
    --border: #0d2d40;
    --text-soft: #8daabf;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-dark) !important;
    font-family: 'Rajdhani', sans-serif !important;
    color: #cce8f4 !important;
}

h1, h2, h3 {
    color: var(--cyan) !important;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.info-card {
    background: linear-gradient(145deg, rgba(10,26,39,0.95), rgba(7,18,30,0.95));
    border: 1px solid var(--border);
    border-left: 4px solid var(--cyan);
    border-radius: 8px;
    padding: 18px 20px;
    margin-bottom: 14px;
}

.mono {
    font-family: 'Share Tech Mono', monospace;
    color: var(--text-soft);
}

.video-title {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.76rem;
    letter-spacing: 1.8px;
    color: var(--cyan);
    text-transform: uppercase;
    margin-bottom: 6px;
}

[data-testid="stVideo"] {
    border: 1px solid var(--border) !important;
    border-top: 2px solid var(--cyan) !important;
    border-radius: 8px !important;
    overflow: hidden !important;
    box-shadow: 0 0 12px rgba(0,229,255,0.22) !important;
}

[data-testid="stButton"] > button:disabled {
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


@st.cache_data(show_spinner=False)
def load_video_bytes(video_path: str):
    p = Path(video_path)
    if not p.exists():
        return None
    return p.read_bytes()


render_top_nav("simulation")
render_simulation_subnav("savunma")
st.markdown("<br>", unsafe_allow_html=True)

st.title("Savunma Mekanizması")
st.markdown(
    '<p class="mono">Tehdit algılama, kaçış manevrası ve karşı önlem sekanslarının simülasyon özeti</p>',
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="info-card">
  <h3>Savunma Akışı</h3>
  <p>
    Savunma mekanizması üç adımda çalışır: <b>tehdit tespiti</b>, <b>kaçış/mesafe açma</b> ve <b>karşı önlem</b>.
    Bu akış, görev güvenliğini korumak için ana berthing kontrolüyle eşzamanlı olarak çalışır.
  </p>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="info-card">
  <h3>Operasyon Notu</h3>
  <p>
    Simülasyon sırasında savunma sekansı tetiklenirse görev durumu güncellenir, olay izi kaydedilir ve
    otonom kontrol sistemi güvenli moda geçer.
  </p>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("---")

col1, col2 = st.columns(2, gap="large")
with col1:
    st.markdown('<div class="video-title">KARSI ONLEM / LAZER VURUSU</div>', unsafe_allow_html=True)
    v1 = load_video_bytes(str(LAZER_VIDEO))
    if v1:
        st.video(v1)
    else:
        st.warning("`assets/LazerVurus.mp4` bulunamadı.")

with col2:
    st.markdown('<div class="video-title">KACIS MANEVRASI / ACIL AYRILMA</div>', unsafe_allow_html=True)
    v2 = load_video_bytes(str(KACIS_VIDEO))
    if v2:
        st.video(v2)
    else:
        st.warning("`assets/Kacis2.mp4` bulunamadı.")

st.markdown("---")
st.markdown("<p style='text-align:center;' class='mono'>GALLIPOLI</p>", unsafe_allow_html=True)
