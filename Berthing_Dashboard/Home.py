import streamlit as st
import base64
import streamlit.components.v1 as components

from pathlib import Path

try:
    from nav import render_top_nav
except ImportError:
    def render_top_nav(page):
        pass

st.set_page_config(
    page_title="TUA Uzay İstasyonu | Ana Sayfa",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Arka plan resmi için güvenli yükleme
bg_image_path = Path(__file__).parent / "assets" / "darker-earth-x.jpg"
if bg_image_path.exists():
    bg_image_b64 = base64.b64encode(bg_image_path.read_bytes()).decode("utf-8")
else:
    bg_image_b64 = ""

home_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@500;700&display=swap');

:root {
    --bg-dark: #040b14;
    --cyan: #00e5ff;
    --card-bg: #0b1f30;
}

html, body, [data-testid="stAppViewContainer"] {
    background:
        linear-gradient(rgba(3, 9, 18, 0.82), rgba(3, 9, 18, 0.82)),
        url("data:image/jpeg;base64,__BG_IMAGE__") no-repeat center center fixed !important;
    background-size: cover !important;
    font-family: 'Rajdhani', sans-serif !important;
    color: #cce8f4 !important;
}

[data-testid="stAppViewContainer"] > .main {
    background: transparent !important;
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 700;
    color: var(--cyan);
    text-transform: uppercase;
    text-align: center;
    letter-spacing: 5px;
    text-shadow: 0 0 20px rgba(0,229,255,0.6);
    margin-bottom: 0;
}

.hero-sub {
    font-family: 'Share Tech Mono', monospace;
    font-size: 1.2rem;
    color: #4a7a96;
    text-align: center;
    letter-spacing: 3px;
    margin-bottom: 14px;
}

.station-stage-title {
    color: var(--cyan);
    font-size: 1.2rem;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.station-stage-sub {
    color: #8daabf;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.85rem;
}

/* ÜZERİNE GELİNCE BÜYÜYEN MODÜL KARTLARI */
.module-card {
    background-color: var(--card-bg);
    border: 1px solid #0d2d40;
    border-left: 4px solid var(--cyan);
    border-radius: 8px;
    padding: 25px;
    height: 240px;
    transition: all 0.3s ease-in-out;
    cursor: pointer;
}

.module-card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 10px 25px rgba(0,229,255,0.3);
    border-color: var(--cyan);
}

.module-icon {
    font-family: 'Share Tech Mono', monospace;
    font-size: 1.1rem;
    font-weight: bold;
    color: #ffb300; /* Amber rengi envanter kodu */
    background: rgba(255, 179, 0, 0.1);
    border: 1px solid rgba(255, 179, 0, 0.4);
    padding: 4px 12px;
    border-radius: 4px;
    display: inline-block;
    margin-bottom: 15px;
    letter-spacing: 2px;
}

.module-title {
    font-weight: 700;
    font-size: 1.4rem;
    color: var(--cyan);
    margin-bottom: 10px;
    text-transform: uppercase;
}

.module-desc {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.9rem;
    color: #8daabf;
    line-height: 1.5;
}

/* BAŞLA BUTONU */
.start-btn-container {
    display: flex;
    justify-content: center;
    margin-top: 50px;
}
</style>
"""
st.markdown(home_css.replace("__BG_IMAGE__", bg_image_b64), unsafe_allow_html=True)

render_top_nav("home")

# --- HERO BÖLÜMÜ ---
st.markdown('<div class="hero-title">TAM OTONOM UZAY İSTASYONU</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">TUA HACKATHON</div>', unsafe_allow_html=True)

try:
    # 3D modeli ortama bagimli olmayan goreli yoldan oku
    model_path = Path(__file__).parent / "assets" / "istasyon.glb"
    with open(model_path, "rb") as f:
        model_data = f.read()
    b64_model = base64.b64encode(model_data).decode("utf-8")
    
    # Google Model Viewer Web Komponenti
    html_code = f"""
    <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.4.0/model-viewer.min.js"></script>
    <model-viewer id="station-model"
                  src="data:model/gltf-binary;base64,{b64_model}" 
                  auto-rotate 
                  rotation-per-second="12deg"
                  orientation="-85deg 0deg 0deg"
                  camera-controls 
                  camera-orbit="42deg 78deg 145%"
                  min-camera-orbit="auto 40deg auto"
                  max-camera-orbit="auto 115deg auto"
                  field-of-view="28deg"
                  shadow-intensity="1"
                  shadow-softness="0.8"
                  tone-mapping="aces"
                  exposure="0.9"
                  environment-image="neutral"
                  interaction-prompt="none"
                  style="width: 100%; height: 380px; background: transparent; outline: none;">
    </model-viewer>
    <script>
      const viewer = document.querySelector('#station-model');
      viewer.addEventListener('load', () => {{
        const palette = [
          [0.38, 0.38, 0.38, 1.00],
          [0.30, 0.30, 0.30, 1.00],
          [0.22, 0.22, 0.22, 1.00]
        ];
        viewer.model?.materials?.forEach((material, idx) => {{
          const pbr = material.pbrMetallicRoughness;
          if (!pbr) return;
          const tone = palette[idx % palette.length];
          pbr.setBaseColorFactor(tone);
          pbr.setMetallicFactor(0.36);
          pbr.setRoughnessFactor(0.44);
        }});
      }});
    </script>
    """
    components.html(html_code, height=390)
except FileNotFoundError:
    st.warning("⚠️ 3D Model (istasyon.glb) assets klasöründe bulunamadı.")
#İSTASYON MODÜLLERİ
st.markdown("<h3 style='text-align: center; color: #4a7a96; font-family: \"Share Tech Mono\";'>İSTASYON MODÜL YAPISI VE İŞLEVSEL KESİTLER</h3><br>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="module-card">
        <div class="module-icon">NODE-01</div>
        <div class="module-title">1. Node Modülü</div>
        <div class="module-desc">İstasyonun ana bağlantı ve modüller arası transfer noktası. Çoklu kenetlenme bağlantı noktaları sağlar.</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="module-card">
        <div class="module-icon">LIFE-02</div>
        <div class="module-title">2. Life Modülü</div>
        <div class="module-desc">Mürettebatın yaşam alanı. Oksijen, su ve sıcaklık kontrolü gibi hayati yaşam destek sistemlerini içerir.</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="module-card">
        <div class="module-icon">CORE-03</div>
        <div class="module-title">3. Core Modülü</div>
        <div class="module-desc">İstasyonun merkezi komuta ve enerji yönetim ünitesi. Seyrüsefer, iletişim ve güç dağıtımını kontrol eder.</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="module-card">
        <div class="module-icon">RES-04</div>
        <div class="module-title">4. Research Modülü</div>
        <div class="module-desc">Bilimsel çalışmalar ve deneyler için mikroçekim laboratuvarı. Uzay gözlemleri ve malzeme araştırmaları yürütür.</div>
    </div>
    """, unsafe_allow_html=True)

# --- SİMÜLASYONA YÖNLENDİRME ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.info("**Test Ortamı Hazır:** Sistemin otonom çalışma ve karar verme süreçlerini canlı görmek için sol menüden **Simülasyon** sayfasına geçiş yapabilirsiniz.")

st.markdown("---")
st.markdown("<p style='text-align:center; font-family: \"Share Tech Mono\"; color: #4a7a96;'>GALLIPOLI</p>", unsafe_allow_html=True)
