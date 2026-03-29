import streamlit as st
from pathlib import Path
from nav import render_top_nav

st.set_page_config(
    page_title="GALLIPOLI TUA HACKATHON | Otonom Mekanizma",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ASSETS_DIR = Path(__file__).resolve().parents[1] / "assets"
GENEL_KAMERA_VIDEO = ASSETS_DIR / "genel_kamera.mp4"
KILIT_ANIM_VIDEO = ASSETS_DIR / "KilitMekanizmasıAnimasyonu.mp4"
ROBOT_ARM_IMAGES = [
    ("ROBOT KOL / GENEL GORUNUM", ASSETS_DIR / "orjinalrobotarm.jpeg"),
    ("KENETLENME MEKANIZMASI SIRASINDA CORE MODULU", ASSETS_DIR / "foto2.jpeg"),
    ("ROBOT KOL / KILIT NOKTASI", ASSETS_DIR / "robot_kol_kilit.png"),
]

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

.image-slot {
    background: linear-gradient(145deg, rgba(10,26,39,0.90), rgba(7,18,30,0.90));
    border: 1px dashed #1e4b62;
    border-top: 2px solid var(--cyan);
    border-radius: 8px;
    padding: 16px;
    min-height: 220px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
}

.image-slot-label {
    font-family: 'Share Tech Mono', monospace;
    color: #7fa5bd;
    font-size: 0.8rem;
    letter-spacing: 1.2px;
    line-height: 1.5;
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

st.title("Otonom Mekanizma")
st.markdown(
    '<p class="mono">Otonom berthing mekanizmasının fazlarını, kilitlenme mantığını ve operasyon akışını açıklayan içerikler</p>',
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="info-card">
  <h3>Mekanizma Akışı</h3>
  <p>
    Otonom mekanizma dört temel fazdan oluşur: <b>yaklaşma</b>, <b>FOD tarama</b>, <b>soft capture</b> ve <b>hard lock</b>.
    Her faz, güvenlik interlock koşulları doğrulanarak bir sonraki aşamaya geçer.
    Simülasyonda canlı telemetri ve olay izi izlenirken, bu sayfadaki videolar mekanik davranışı görsel olarak özetler.
  </p>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="info-card">
  <h3>Operasyon Rehberi</h3>
  <p>
    1) <b>Simülasyon</b> sekmesine geçin.<br>
    2) Senaryoyu seçin (Temiz Yüzey / FOD).<br>
    3) <b>Otonom Sekansı Başlat</b> ile mekanizma döngüsünü çalıştırın.<br>
    4) Faz geçişleri, interlock kontrolleri ve kilitlenme durumlarını takip edin.
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
    st.markdown('<div class="video-title">KENETLENME MEKANİZMASI</div>', unsafe_allow_html=True)
    v2 = load_video_bytes(str(KILIT_ANIM_VIDEO))
    if v2:
        st.video(v2)
    else:
        st.warning("`assets/KilitMekanizmasıAnimasyonu.mp4` bulunamadı.")

st.markdown("---")
st.markdown('<div class="video-title">ROBOT KOL GORSEL ALANI / HAZIR SLOTLAR</div>', unsafe_allow_html=True)
slot_cols = st.columns(3, gap="large")

for col, (label, image_path) in zip(slot_cols, ROBOT_ARM_IMAGES):
    with col:
        st.markdown(f'<div class="video-title">{label}</div>', unsafe_allow_html=True)
        if image_path.exists():
            st.image(str(image_path), use_container_width=True)
        else:
            st.markdown(
                f"""
                <div class="image-slot">
                    <div class="image-slot-label">
                        {image_path.name} dosyasi bekleniyor.<br>
                        Dosyayi <b>assets/</b> klasorune eklediginizde otomatik goruntulenecek.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

st.markdown(
    '<p class="mono">Desteklenen ornek dosya adlari: `orjinalrobotarm.jpeg`, `foto2.jpeg`, `robot_kol_kilit.png`</p>',
    unsafe_allow_html=True,
)

st.markdown("---")
st.markdown("<p style='text-align:center;' class='mono'>GALLIPOLI</p>", unsafe_allow_html=True)
