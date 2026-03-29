import streamlit as st
from nav import render_top_nav

st.set_page_config(
    page_title="GALLIPOLI TUA HACKATHON | Hakkımızda",
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
    Tam Otonom Uzay İstasyonu için geliştirilen bu çözüm, robotik kol tabanlı otonom hizalama ve kenetlenme işlemlerini, optik FOD tespiti ve güvenlik odaklı karar verme süreçlerini tek bir görev kontrol akışında birleştirir.
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

st.markdown('<h3 style="margin-top:8px;">Takım</h3>', unsafe_allow_html=True)

team_members = [
    {
        "name": "Arda Kıvanç ÖZDEMİR",
        "role": "Takım Lideri",
        "education": "Başkent Üniversitesi · Makine Mühendisliği · 3. sınıf (Onur Öğrencisi)",
        "bio": (
            "TEKNOFEST 2024 Tarımsal İKA yarışmasında mekanik tasarım yetkinliğiyle Türkiye 8.liği "
            "başarısı elde etmiş, TEKNOFEST 2025 Uluslararası İHA projelerinde yapısal tasarım ve "
            "analiz çalışmalarında yer almıştır. Takımda hibrit motorun matematiksel modellenmesi, "
            "besleme sistemi tasarımı ve statik ateşleme düzeneğinin geliştirilmesi süreçlerini yönetmektedir."
        ),
    },
    {
        "name": "Şaban Efe ŞAHİN",
        "role": "Üretim ve Montaj Lideri",
        "education": "Gazi Üniversitesi · Uçak Teknolojisi · 2. sınıf",
        "bio": (
            "Savunma sanayi odaklı İHA projelerinde üretim ve montaj tecrübesine sahiptir. "
            "TEKNOFEST 2025 Uluslararası İHA Yarışması'nda pilotu olduğu takımı ile finallerde yarışmıştır. "
            "Takımda 3D tasarım, imalat koordinasyonu, tedarik süreçleri ve motorun fiziksel montaj "
            "aşamalarına liderlik etmektedir."
        ),
    },
    {
        "name": "Enes OZAN",
        "role": "Mekanik Tasarım ve İmalat",
        "education": "Başkent Üniversitesi · Makine Mühendisliği · 3. sınıf",
        "bio": (
            "Lise eğitiminde edindiği uçak gövde-motor altyapısını, üniversite sürecindeki talaşlı "
            "imalat ve CNC staj deneyimleriyle birleştirerek takımda malzeme seçimi, mekanik tasarım "
            "ve montaj planlama süreçlerine teknik katkı sunmaktadır."
        ),
    },
    {
        "name": "Eyüp Efe ASLAN",
        "role": "Yazılım ve Veri Süreçleri",
        "education": "Ankara Üniversitesi · Yazılım Mühendisliği · 2. sınıf",
        "bio": (
            "VoIP mimarileri, AI tabanlı sosyal medya güvenliği ve radyo frekansı teknolojileri "
            "üzerine staj ve çalışma deneyimine sahiptir. Full stack web teknolojileri alanında "
            "projeler yürütmektedir. Takımda HRAP verilerine göre roket boyutlandırma ve motor test "
            "verilerinin kontrolü süreçlerini yürütmektedir."
        ),
    },
]

for i in range(0, len(team_members), 2):
    c1, c2 = st.columns(2, gap="large")
    pair = team_members[i:i + 2]
    for col, member in zip([c1, c2], pair):
        with col:
            st.markdown(
                f"""
                <div class="info-card">
                  <h3>{member["name"]}</h3>
                  <p class="mono">{member["role"]}</p>
                  <p><b>{member["education"]}</b></p>
                  <p>{member["bio"]}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

st.markdown("---")
st.markdown("<p style='text-align:center;' class='mono'>GALLIPOLI</p>", unsafe_allow_html=True)
