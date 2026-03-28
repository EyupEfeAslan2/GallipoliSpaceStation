import streamlit as st
from nav import render_top_nav

st.set_page_config(
    page_title="TUA Uzay İstasyonu | Hakkımızda",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
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
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-left: 4px solid var(--cyan);
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 16px;
}

.mono {
    font-family: 'Share Tech Mono', monospace;
    color: var(--text-soft);
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
""", unsafe_allow_html=True)


render_top_nav("about")
st.markdown("<br>", unsafe_allow_html=True)

st.title("Hakkımızda")
st.markdown('<p class="mono">TUA Hackathon · Otonom Berthing & Savunma Mimarisi</p>', unsafe_allow_html=True)

st.markdown("""
<div class="info-card">
  <h3>Proje Vizyonu</h3>
  <p>
    LEO-DOCK-3 uzay istasyonu için geliştirilen bu çözüm, robotik kol tabanlı otonom kenetlenme,
    optik FOD tespiti ve güvenlik odaklı karar verme süreçlerini tek bir görev kontrol akışında birleştirir.
  </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-card">
  <h3>Temel Kabiliyetler</h3>
  <p>
    • Otonom yaklaşma ve hizalama<br>
    • OpenCV tabanlı yabancı cisim (FOD) algılama<br>
    • UDP üzerinden Unity simülasyonu ile haberleşme<br>
    • Hard berthing aşamasında görev durumu ve telemetri takibi
  </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align:center;' class='mono'>© 2026 TUA Hackathon Takımı</p>", unsafe_allow_html=True)
