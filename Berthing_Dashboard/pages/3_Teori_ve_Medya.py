import streamlit as st
from pathlib import Path
from nav import render_top_nav

st.set_page_config(
    page_title="GALLIPOLI TUA HACKATHON | Teori ve Medya",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ASSETS_DIR = Path(__file__).resolve().parents[1] / "assets"
GENEL_KAMERA_VIDEO = ASSETS_DIR / "genel_kamera.mp4"
KILIT_ANIM_VIDEO = ASSETS_DIR / "KilitMekanizmasıAnimasyonu.mp4"

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


render_top_nav("theory")
st.markdown("<br>", unsafe_allow_html=True)

st.title("Teori ve Medya")
st.markdown('<p class="mono">Otonom berthing görevini anlatan videolar ve kullanım özeti</p>', unsafe_allow_html=True)

st.markdown(
    """
<div class="info-card">
  <h3>Nasıl Çalışır?</h3>
  <p>
    Sistem dört fazda çalışır: <b>yaklaşma</b>, <b>FOD tarama</b>, <b>soft capture</b> ve <b>hard lock</b>.
    Simülasyon ekranı canlı telemetri, interlock kontrolleri ve olay izini verir.
    Bu sayfadaki videolar ise aynı akışın genel mantığını görsel olarak özetler.
  </p>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="info-card">
  <h3>Kullanım Kısa Rehberi</h3>
  <p>
    1) <b>Simülasyon</b> sekmesine geçin.<br>
    2) Senaryoyu seçin (Temiz Yüzey / FOD).<br>
    3) <b>Otonom Sekansı Başlat</b> ile görevi çalıştırın.<br>
    4) KPI, event trace ve interlock sonuçlarını takip edin.
  </p>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("---")

col1, col2 = st.columns(2, gap="large")
with col1:
    st.markdown('<div class="video-title">GENEL KAMERA / YAKLAŞMA VE HİZALAMA</div>', unsafe_allow_html=True)
    v1 = load_video_bytes(str(GENEL_KAMERA_VIDEO))
    if v1:
        st.video(v1)
    else:
        st.warning("`assets/genel_kamera.mp4` bulunamadı.")

with col2:
    st.markdown('<div class="video-title">KİLİT MEKANİZMASI / HARD LOCK</div>', unsafe_allow_html=True)
    v2 = load_video_bytes(str(KILIT_ANIM_VIDEO))
    if v2:
        st.video(v2)
    else:
        st.warning("`assets/KilitMekanizmasıAnimasyonu.mp4` bulunamadı.")

st.markdown("---")
st.markdown("<p style='text-align:center;' class='mono'>GALLIPOLI</p>", unsafe_allow_html=True)
