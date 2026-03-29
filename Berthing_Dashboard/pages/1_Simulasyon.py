import streamlit as st
import cv2
import numpy as np
import time
import socket
import math
import io
import csv
import json
from pathlib import Path
from nav import render_top_nav

# ═══════════════════════════════════════════════════════════
#  SAYFA AYARLARI
# ═══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="TUA - Otonom Berthing Gorev Kontrolu",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ASSETS_DIR = Path(__file__).resolve().parents[1] / "assets"
GENEL_KAMERA_VIDEO = ASSETS_DIR / "genel_kamera.mp4"
KILIT_ANIM_VIDEO = ASSETS_DIR / "KilitMekanizmasıAnimasyonu.mp4"

# ═══════════════════════════════════════════════════════════
#  GLOBAL CSS - Futuristik / Karanlik Tema
# ═══════════════════════════════════════════════════════════
st.markdown("""
<style>
/* ── Google Font yükle ── */
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;500;600;700&display=swap');

/* ── Kök değişkenler ── */
:root {
    --bg-primary:   #040b14;
    --bg-panel:     #071220;
    --bg-card:      #0b1f30;
    --accent-cyan:  #00e5ff;
    --accent-green: #00ff9d;
    --accent-red:   #ff3c5a;
    --accent-amber: #ffb300;
    --text-primary: #cce8f4;
    --text-dim:     #4a7a96;
    --border:       #0d2d40;
    --glow-cyan:    0 0 12px rgba(0,229,255,0.45);
    --glow-green:   0 0 12px rgba(0,255,157,0.45);
    --glow-red:     0 0 12px rgba(255,60,90,0.50);
}

/* ── Genel zemin ── */
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background-color: var(--bg-primary) !important;
    font-family: 'Rajdhani', sans-serif !important;
    color: var(--text-primary) !important;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { background-color: var(--bg-panel) !important; }

/* ── Tüm markdown / text rengi ── */
p, label, div { color: var(--text-primary) !important; font-family: 'Rajdhani', sans-serif !important; }

/* ── Başlıklar ── */
h1, h2, h3, h4 {
    font-family: 'Rajdhani', sans-serif !important;
    color: var(--accent-cyan) !important;
    letter-spacing: 2px;
    text-transform: uppercase;
}

/* ── Metric kartları ── */
[data-testid="stMetricValue"] {
    font-family: 'Share Tech Mono', monospace !important;
    color: var(--accent-cyan) !important;
    font-size: 1.6rem !important;
    text-shadow: var(--glow-cyan);
}
[data-testid="stMetricLabel"] {
    font-family: 'Rajdhani', sans-serif !important;
    color: var(--text-dim) !important;
    font-size: 0.72rem !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}
[data-testid="stMetricDelta"] { font-family: 'Share Tech Mono', monospace !important; }
[data-testid="metric-container"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-left: 3px solid var(--accent-cyan) !important;
    border-radius: 4px !important;
    padding: 14px 18px !important;
    box-shadow: var(--glow-cyan);
}

/* ── Progress bar ── */
[data-testid="stProgress"] > div > div > div > div {
    background: linear-gradient(90deg, #003d52, var(--accent-cyan)) !important;
    box-shadow: var(--glow-cyan);
}
[data-testid="stProgress"] > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 2px !important;
}

/* ── Buton ── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #003d52 0%, #004d66 100%) !important;
    color: var(--accent-cyan) !important;
    border: 1px solid var(--accent-cyan) !important;
    border-radius: 3px !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 1rem !important;
    letter-spacing: 3px;
    text-transform: uppercase;
    box-shadow: var(--glow-cyan);
    transition: all 0.2s ease !important;
}
[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #004d66 0%, #006680 100%) !important;
    box-shadow: 0 0 22px rgba(0,229,255,0.7) !important;
    transform: scale(1.01);
}
[data-testid="stButton"] > button:disabled {
    background: #0a0f14 !important;
    color: #6d7c88 !important;
    border: 1px solid #1b2731 !important;
    box-shadow: none !important;
    cursor: not-allowed !important;
    opacity: 1 !important;
}

/* ── Radio buton ── */
[data-testid="stRadio"] label {
    color: var(--text-primary) !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.95rem;
    letter-spacing: 1px;
}

/* ── Alert renkleri ── */
[data-testid="stAlert"] {
    border-radius: 3px !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1rem;
    letter-spacing: 0.5px;
}

/* ── Ayırıcı çizgi ── */
hr { border-color: var(--border) !important; }

/* ── Image caption ── */
[data-testid="caption"] {
    color: var(--text-dim) !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* ── Column container boşluk ── */
[data-testid="stVerticalBlock"] { gap: 0.6rem; }

/* ── Özel panel kutusu ── */
.panel-box {
    background: var(--bg-panel);
    border: 1px solid var(--border);
    border-top: 2px solid var(--accent-cyan);
    border-radius: 4px;
    padding: 16px 20px;
    margin-bottom: 10px;
}
.panel-title {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.72rem;
    color: var(--accent-cyan);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 10px;
    opacity: 0.75;
}
.status-badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 2px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.78rem;
    letter-spacing: 2px;
    text-transform: uppercase;
}
.badge-standby  { background:#001520; color:#4a9ab0; border:1px solid #0d3040; }
.badge-active   { background:#001a0a; color:var(--accent-green); border:1px solid #004020; box-shadow:var(--glow-green); }
.badge-warning  { background:#1a1000; color:var(--accent-amber); border:1px solid #3a2800; }
.badge-critical { background:#1a0008; color:var(--accent-red);   border:1px solid #3a0015; box-shadow:var(--glow-red); }

.faz-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.68rem;
    color: var(--text-dim);
    letter-spacing: 2px;
    text-transform: uppercase;
}
.faz-value {
    font-family: 'Share Tech Mono', monospace;
    font-size: 1.05rem;
    color: var(--accent-cyan);
    text-shadow: var(--glow-cyan);
}

/* ── Header banner ── */
.header-banner {
    background: linear-gradient(90deg, var(--bg-panel), #061828, var(--bg-panel));
    border: 1px solid var(--border);
    border-bottom: 2px solid var(--accent-cyan);
    padding: 18px 28px;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 20px;
}
.header-title {
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    font-size: 1.6rem;
    color: var(--accent-cyan);
    letter-spacing: 4px;
    text-transform: uppercase;
    text-shadow: var(--glow-cyan);
}
.header-sub {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    color: var(--text-dim);
    letter-spacing: 3px;
    text-transform: uppercase;
}
.mission-id {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75rem;
    color: var(--accent-amber);
    letter-spacing: 2px;
    margin-left: auto;
}

.kpi-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent-cyan);
    border-radius: 6px;
    padding: 12px 14px;
    min-height: 102px;
}
.kpi-title {
    font-size: 0.72rem;
    letter-spacing: 1.4px;
    color: var(--text-dim);
    text-transform: uppercase;
}
.kpi-value {
    margin-top: 4px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 1.15rem;
    color: var(--text-primary);
}
.kpi-threshold {
    margin-top: 7px;
    font-size: 0.68rem;
    color: var(--text-dim);
}

.interlock-row {
    display: grid;
    grid-template-columns: 1fr auto;
    align-items: center;
    background: var(--bg-panel);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 9px 12px;
    margin-bottom: 8px;
}
.interlock-label {
    font-size: 0.82rem;
    letter-spacing: 0.5px;
}
.interlock-status {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 1.2px;
    border-radius: 3px;
    padding: 3px 9px;
    border: 1px solid var(--border);
}

.trace-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.78rem;
}
.trace-table th, .trace-table td {
    border-bottom: 1px solid var(--border);
    padding: 6px 7px;
    text-align: left;
}
.trace-table th {
    color: var(--text-dim);
    letter-spacing: 1px;
    text-transform: uppercase;
    font-size: 0.66rem;
}

.milestone-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px;
}
.milestone-card {
    background: var(--bg-panel);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 10px 12px;
}
.milestone-title {
    font-size: 0.76rem;
    color: var(--accent-cyan);
    text-transform: uppercase;
    letter-spacing: 1px;
}
.milestone-meta {
    margin-top: 6px;
    font-size: 0.72rem;
    color: var(--text-dim);
}

.video-brief {
    background: linear-gradient(90deg, #06121f, #082034, #06121f);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent-cyan);
    border-radius: 6px;
    padding: 12px 14px;
    margin-bottom: 10px;
}
.video-brief-title {
    font-family: 'Share Tech Mono', monospace;
    color: var(--accent-cyan);
    letter-spacing: 2px;
    font-size: 0.76rem;
    text-transform: uppercase;
}
.video-brief-sub {
    margin-top: 4px;
    color: var(--text-dim);
    font-size: 0.9rem;
}
.video-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 1.6px;
    text-transform: uppercase;
    color: var(--accent-cyan);
    margin-bottom: 6px;
}
[data-testid="stVideo"] {
    border: 1px solid var(--border) !important;
    border-top: 2px solid var(--accent-cyan) !important;
    border-radius: 8px !important;
    overflow: hidden !important;
    box-shadow: var(--glow-cyan) !important;
}

/* scrollbar */
::-webkit-scrollbar { width:4px; background:var(--bg-primary); }
::-webkit-scrollbar-thumb { background:var(--border); border-radius:2px; }
</style>
""", unsafe_allow_html=True)

render_top_nav("simulation")
st.markdown("<br>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
#  YARDIMCI FONKSİYONLAR
# ═══════════════════════════════════════════════════════════

def generate_mock_image(has_fod: bool) -> np.ndarray:
    """Dock yüzeyi sahte görüntüsü üretir."""
    img = np.zeros((480, 640, 3), dtype=np.uint8)

    # Yıldız arka planı
    rng = np.random.default_rng(42)
    for _ in range(220):
        # np.int64 -> saf Python int (OpenCV 4.x zorunlulugu)
        sx = int(rng.integers(0, 640))
        sy = int(rng.integers(0, 480))
        b  = int(rng.integers(60, 180))
        cv2.circle(img, (sx, sy), 1, (b, b, b), -1)

    # Dock halka yapısı (birden fazla halka)
    cx, cy = 320, 240
    cv2.circle(img, (cx, cy), 160, (0, 60, 80), 2)
    cv2.circle(img, (cx, cy), 100, (0, 80, 110), 2)
    cv2.circle(img, (cx, cy), 40,  (0, 100, 130), 2)

    # Kılavuz çizgileri
    cv2.line(img, (cx - 170, cy), (cx + 170, cy), (0, 40, 60), 1)
    cv2.line(img, (cx, cy - 170), (cx, cy + 170), (0, 40, 60), 1)

    # Hizalama köşe işaretleri
    for angle_deg in [45, 135, 225, 315]:
        angle = math.radians(angle_deg)
        x1 = int(cx + 120 * math.cos(angle))
        y1 = int(cy + 120 * math.sin(angle))
        cv2.circle(img, (x1, y1), 6, (0, 150, 180), -1)

    # Merkez hedef
    cv2.circle(img, (cx, cy), 12, (0, 200, 230), -1)
    cv2.circle(img, (cx, cy), 4,  (255, 255, 255), -1)

    # Tarama çizgisi efekti (yatay yeşil scan line)
    scan_y = 140
    for i in range(4):
        alpha_line = np.zeros_like(img, dtype=np.uint8)
        cv2.line(alpha_line, (0, scan_y + i * 50), (640, scan_y + i * 50), (0, 30, 20), 1)
        img = cv2.addWeighted(img, 1.0, alpha_line, 0.4, 0)

    if has_fod:
        # FOD 1 - buyuk parca
        cv2.circle(img, (390, 170), 22, (210, 210, 210), -1)
        cv2.circle(img, (390, 170), 22, (255, 255, 255),  1)
        # FOD 2 - kucuk parca
        cv2.circle(img, (260, 310), 10, (180, 180, 180), -1)

    return img


def detect_and_annotate(image: np.ndarray):
    """Parlak yabancı nesneleri tespit eder ve görüntüyü anotasyonlar."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 190, 255, cv2.THRESH_BINARY)

    # Morfolojik açma: gürültü azalt
    kernel = np.ones((3, 3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    fod_list = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 60:
            x, y, w, h = cv2.boundingRect(cnt)
            fod_list.append((x, y, w, h, area))

    annotated = image.copy()

    if fod_list:
        # Kırmızı alarm overlay
        overlay = annotated.copy()
        cv2.rectangle(overlay, (0, 0), (639, 479), (0, 0, 180), -1)
        annotated = cv2.addWeighted(annotated, 0.85, overlay, 0.15, 0)

        for idx, (x, y, w, h, area) in enumerate(fod_list):
            # Köşe L-parantezleri (NASA tarzı)
            length = 18
            thickness = 2
            color = (0, 0, 255)
            # Sol-üst
            cv2.line(annotated, (x - 6, y - 6), (x - 6 + length, y - 6), color, thickness)
            cv2.line(annotated, (x - 6, y - 6), (x - 6, y - 6 + length), color, thickness)
            # Sağ-üst
            cv2.line(annotated, (x + w + 6, y - 6), (x + w + 6 - length, y - 6), color, thickness)
            cv2.line(annotated, (x + w + 6, y - 6), (x + w + 6, y - 6 + length), color, thickness)
            # Sol-alt
            cv2.line(annotated, (x - 6, y + h + 6), (x - 6 + length, y + h + 6), color, thickness)
            cv2.line(annotated, (x - 6, y + h + 6), (x - 6, y + h + 6 - length), color, thickness)
            # Sağ-alt
            cv2.line(annotated, (x + w + 6, y + h + 6), (x + w + 6 - length, y + h + 6), color, thickness)
            cv2.line(annotated, (x + w + 6, y + h + 6), (x + w + 6, y + h + 6 - length), color, thickness)

            label = f"FOD-{idx+1:02d}  ALAN:{int(area)}px2"
            cv2.putText(annotated, label, (x - 6, y - 14),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 80, 255), 1, cv2.LINE_AA)

        # Üst banner
        cv2.rectangle(annotated, (0, 0), (639, 32), (0, 0, 100), -1)
        cv2.putText(annotated, "!! KRITIK UYARI: YABANCI CISIM TESPIT EDILDI !!",
                    (12, 21), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 60, 255), 1, cv2.LINE_AA)
    else:
        # Yeşil onay overlay
        cv2.rectangle(annotated, (0, 0), (639, 32), (0, 60, 20), -1)
        cv2.putText(annotated, "CV TARAMA: TEMIZ (GO)  //  FOD ALGILAMA: NEGATIF",
                    (12, 21), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 100), 1, cv2.LINE_AA)
        # Yeşil merkez onay halkası
        cx, cy = 320, 240
        cv2.circle(annotated, (cx, cy), 165, (0, 200, 80), 2)
        cv2.putText(annotated, "CLEAR", (cx - 28, cy + 185),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 200, 80), 1, cv2.LINE_AA)

    # Zaman damgası
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ")
    cv2.putText(annotated, ts, (10, 470),
                cv2.FONT_HERSHEY_SIMPLEX, 0.38, (0, 80, 100), 1, cv2.LINE_AA)
    cv2.putText(annotated, "TUA-ARM-CAM-01", (480, 470),
                cv2.FONT_HERSHEY_SIMPLEX, 0.38, (0, 80, 100), 1, cv2.LINE_AA)

    return annotated, len(fod_list) > 0


def send_udp_command(command: str, ip: str = "127.0.0.1", port: int = 5005):
    """Unity'ye UDP komutu gönderir."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1.0)
        sock.sendto(command.encode("utf-8"), (ip, port))
        sock.close()
        return True
    except Exception:
        return False


def _status_style(status: str):
    status = status.upper()
    if status in {"PASS", "SUCCESS"}:
        return "#002315", "#00ff9d", "#004020"
    if status in {"WARN", "DEGRADED"}:
        return "#1a1000", "#ffb300", "#3a2800"
    if status in {"FAIL", "TRIPPED", "ABORT"}:
        return "#1a0008", "#ff3c5a", "#3a0015"
    return "#001520", "#4a9ab0", "#0d3040"


def _kpi_eval(value, pass_max=None, warn_max=None):
    if value is None:
        return "N/A"
    if pass_max is not None and value <= pass_max:
        return "PASS"
    if warn_max is not None and value <= warn_max:
        return "WARN"
    return "FAIL"


def render_kpi_cards(placeholders, kpi):
    cards = [
        ("Final Alignment Error", f"{kpi['alignment_error_deg']:.3f} deg" if kpi["alignment_error_deg"] is not None else "N/A",
         "<=0.20 PASS / <=0.50 WARN",
         _kpi_eval(kpi["alignment_error_deg"], 0.20, 0.50)),
        ("Time To Dock", f"{kpi['time_to_dock_s']:.2f}s" if kpi["time_to_dock_s"] is not None else "N/A",
         "<=35s PASS / <=50s WARN",
         _kpi_eval(kpi["time_to_dock_s"], 35.0, 50.0)),
        ("Max Contact Force", f"{kpi['max_contact_force_n']:.1f}N" if kpi["max_contact_force_n"] is not None else "N/A",
         "<=40N PASS / <=50N WARN",
         _kpi_eval(kpi["max_contact_force_n"], 40.0, 50.0)),
        ("FOD Detection Latency", f"{kpi['fod_detection_latency_s']:.3f}s" if kpi["fod_detection_latency_s"] is not None else "N/A",
         "<=0.70s PASS / <=1.50s WARN",
         _kpi_eval(kpi["fod_detection_latency_s"], 0.70, 1.50) if kpi["fod_detection_latency_s"] is not None else "N/A"),
        ("Abort Reaction Time", f"{kpi['abort_reaction_ms']:.1f}ms" if kpi["abort_reaction_ms"] is not None else "N/A",
         "<=400ms PASS / <=800ms WARN",
         _kpi_eval(kpi["abort_reaction_ms"], 400.0, 800.0) if kpi["abort_reaction_ms"] is not None else "N/A"),
        ("Mission Result", kpi["mission_result"], "SUCCESS / ABORT / PENDING",
         "SUCCESS" if kpi["mission_result"] == "SUCCESS" else ("ABORT" if kpi["mission_result"] == "ABORT" else "N/A")),
    ]
    for ph, (title, value, threshold, status) in zip(placeholders, cards):
        bg, fg, border = _status_style(status)
        ph.markdown(
            f"""
            <div class="kpi-card" style="border-left-color:{fg};">
                <div class="kpi-title">{title}</div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-threshold">{threshold}</div>
                <div class="kpi-threshold" style="color:{fg};">Status: {status}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_interlocks(ph, interlocks):
    rows = []
    for label, state in interlocks.items():
        bg, fg, border = _status_style(state)
        rows.append(
            f"""
            <div class="interlock-row">
              <div class="interlock-label">{label}</div>
              <div class="interlock-status" style="background:{bg};color:{fg};border-color:{border};">{state}</div>
            </div>
            """
        )
    ph.markdown("".join(rows), unsafe_allow_html=True)


def render_event_trace(ph, events):
    if not events:
        ph.markdown("<div class='kpi-threshold'>Henüz olay kaydı yok.</div>", unsafe_allow_html=True)
        return

    rows = []
    for e in events[-14:]:
        _, fg, _ = _status_style(e["severity"])
        rows.append(
            "<tr>"
            f"<td>{e['t_plus']}</td>"
            f"<td>{e['source']}</td>"
            f"<td style='color:{fg};'>{e['severity']}</td>"
            f"<td>{e['event']}</td>"
            f"<td>{e['detail']}</td>"
            "</tr>"
        )
    ph.markdown(
        "<table class='trace-table'>"
        "<thead><tr><th>T+</th><th>Source</th><th>Severity</th><th>Event</th><th>Detail</th></tr></thead>"
        "<tbody>" + "".join(rows) + "</tbody></table>",
        unsafe_allow_html=True
    )


def render_milestones(ph, milestones):
    cards = []
    for m in milestones:
        status = "READY" if m["actual_t_plus"] else "PENDING"
        _, fg, _ = _status_style("SUCCESS" if status == "READY" else "WARN")
        cards.append(
            f"""
            <div class="milestone-card">
              <div class="milestone-title">{m['label']}</div>
              <div class="milestone-meta">Expected: {m['expected_window']}</div>
              <div class="milestone-meta">Actual: {m['actual_t_plus'] or 'Pending (Unity video timestamp bekleniyor)'}</div>
              <div class="milestone-meta">Status: <span style="color:{fg};">{status}</span></div>
            </div>
            """
        )
    ph.markdown(f"<div class='milestone-grid'>{''.join(cards)}</div>", unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def load_video_bytes(video_path: str):
    path = Path(video_path)
    if not path.exists():
        return None
    return path.read_bytes()

# ═══════════════════════════════════════════════════════════
#  HEADER BANNER
# ═══════════════════════════════════════════════════════════
st.markdown("""
<div class="header-banner">
  <div>
    <div class="header-title">TUA - Otonom Berthing GKS</div>
    <div class="header-sub">Gorev Kontrol Sistemi - Robotik Kol Berthing Otomasyon Modulu v2.1</div>
  </div>
  <div class="mission-id">MİSYON ID: TUA-2025-HB-042 &nbsp;|&nbsp; PLATFORM: LEO-DOCK-3</div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#  ÜST METRİK ŞERIDI
# ═══════════════════════════════════════════════════════════
m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
m_col1.metric("Sistem Durumu",   "STANDBY",   "Bekleniyor")
m_col2.metric("UDP Bağlantısı",  "127.0.0.1:5005", "Unity Simülatörü")
m_col3.metric("Kol Konumu (m)",  "10.00",     "+/-0.002")
m_col4.metric("Yonelim (deg)",   "0.00",      "Roll/Pitch/Yaw")
m_col5.metric("Batarya",         "%94",       "Nominal")

st.markdown("---")

# ═══════════════════════════════════════════════════════════
#  GÖREV İŞLEYİŞ ÖNİZLEME VİDEOLARI
# ═══════════════════════════════════════════════════════════
st.markdown('<div class="panel-title">GÖREV İŞLEYİŞ ÖNİZLEME</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="video-brief">
      <div class="video-brief-title">Görev Akış Özeti</div>
      <div class="video-brief-sub">
        Sol video istasyonla hizalama ve yaklaşma akışını, sağ video ise kenetlenme/kilit mekanizmasının
        çalışma adımlarını gösterir. İkisi birlikte berthing sürecinin genel mantığını anlatır.
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)
vcol1, vcol2 = st.columns(2, gap="large")
with vcol1:
    st.markdown('<div class="video-label">GENEL KAMERA / YAKLAŞMA AKIŞI</div>', unsafe_allow_html=True)
    genel_kamera_data = load_video_bytes(str(GENEL_KAMERA_VIDEO))
    if genel_kamera_data:
        st.video(genel_kamera_data, autoplay=True, muted=True, loop=True)
    else:
        st.warning("`assets/genel_kamera.mp4` bulunamadı.")
with vcol2:
    st.markdown('<div class="video-label">KİLİT MEKANİZMASI / HARD LOCK ANİMASYONU</div>', unsafe_allow_html=True)
    kilit_anim_data = load_video_bytes(str(KILIT_ANIM_VIDEO))
    if kilit_anim_data:
        st.video(kilit_anim_data, autoplay=True, muted=True, loop=True)
    else:
        st.warning("`assets/KilitMekanizmasıAnimasyonu.mp4` bulunamadı.")

st.markdown("---")

# ═══════════════════════════════════════════════════════════
#  KPI PANELI
# ═══════════════════════════════════════════════════════════
st.markdown('<div class="panel-title">KPI PANELI</div>', unsafe_allow_html=True)
kpi_row1 = st.columns(3)
kpi_row2 = st.columns(3)
kpi_placeholders = [c.empty() for c in kpi_row1 + kpi_row2]
kpi_state = {
    "alignment_error_deg": None,
    "time_to_dock_s": None,
    "max_contact_force_n": 0.0,
    "fod_detection_latency_s": None,
    "abort_reaction_ms": None,
    "mission_result": "PENDING",
}
render_kpi_cards(kpi_placeholders, kpi_state)

st.markdown("---")

# ═══════════════════════════════════════════════════════════
#  ANA PANEL: sol - kamera | sag - telemetri
# ═══════════════════════════════════════════════════════════
left_col, right_col = st.columns([3, 2], gap="large")

with left_col:
    st.markdown('<div class="panel-title">Optik Hizalama ve FOD Tarama Kamerası</div>', unsafe_allow_html=True)
    camera_ph = st.empty()
    # Başlangıç görüntüsü
    init_img = np.zeros((480, 640, 3), dtype=np.uint8)
    cv2.putText(init_img, "KAMERA BEKLENIYOR...", (160, 235),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 80, 100), 1, cv2.LINE_AA)
    cv2.rectangle(init_img, (0, 0), (639, 479), (0, 40, 60), 1)
    camera_ph.image(cv2.cvtColor(init_img, cv2.COLOR_BGR2RGB),
                    use_container_width=True,
                    caption="ARM-CAM-01 - Docking Yuzeyi Kamerasi")

with right_col:
    st.markdown('<div class="panel-title">Sistem Durumu ve Telemetri</div>', unsafe_allow_html=True)

    status_ph    = st.empty()
    status_ph.info("Sistem bekleme modunda. Sekansı başlatmak için butona basın.")

    st.markdown("**BERTHING FAZ DURUMU**")
    faz_cols = st.columns(4)
    faz_labels  = ["F1: YAKLAŞMA", "F2: TARAMA", "F3: SOFT CAP", "F4: HARD LOCK"]
    faz_placeholders = [col.empty() for col in faz_cols]

    def render_faz_badges(active_index: int, error: bool = False):
        for i, (col, label) in enumerate(zip(faz_cols, faz_labels)):
            if i < active_index:
                col.markdown(f'<div class="status-badge badge-active">OK</div><div class="faz-label">{label}</div>', unsafe_allow_html=True)
            elif i == active_index:
                badge_cls = "badge-critical" if error else "badge-warning"
                col.markdown(f'<div class="status-badge {badge_cls}">></div><div class="faz-label">{label}</div>', unsafe_allow_html=True)
            else:
                col.markdown(f'<div class="status-badge badge-standby">IDLE</div><div class="faz-label">{label}</div>', unsafe_allow_html=True)

    render_faz_badges(-1)

    st.markdown("---")
    st.markdown("**ALTI KANALLİ TELEMETRI**")
    tel_c1, tel_c2 = st.columns(2)
    dist_ph  = tel_c1.empty()
    vel_ph   = tel_c2.empty()
    roll_ph  = tel_c1.empty()
    pitch_ph = tel_c2.empty()
    force_ph = tel_c1.empty()
    hcs_ph   = tel_c2.empty()

    def update_telemetry(dist, vel, roll=0.0, pitch=0.0, force=0.0, hcs="KAPALI"):
        dist_ph.metric("Mesafe (m)",    f"{dist:.2f}", f"{-vel*0.1:.3f}")
        vel_ph.metric("Yakl. Hızı (cm/s)", f"{vel:.1f}",  "nominal")
        roll_ph.metric("Roll (deg)",  f"{roll:.2f}",  "+/-0.01")
        pitch_ph.metric("Pitch (deg)", f"{pitch:.2f}", "+/-0.01")
        force_ph.metric("Temas Kuvveti (N)", f"{force:.1f}", "")
        hcs_ph.metric("HCS Vidaları", hcs, "")

    update_telemetry(10.00, 0.0)

    st.markdown("---")
    st.markdown("**UDP BAĞLANTI DURUMU**")
    udp_ph = st.empty()
    udp_ph.markdown('<span class="status-badge badge-standby">UDP PASIF</span>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
#  İLERLEME ÇUBUĞU
# ═══════════════════════════════════════════════════════════
st.markdown("---")
st.markdown('<div class="panel-title">MİSYON İLERLEME DURUMU</div>', unsafe_allow_html=True)
progress_ph = st.progress(0)
progress_label_ph = st.empty()
progress_label_ph.markdown('<span class="faz-value">%0 - Bekleniyor</span>', unsafe_allow_html=True)

st.markdown("---")

# ═══════════════════════════════════════════════════════════
#  SENARYO SEÇİMİ & BAŞLAT BUTONU
# ═══════════════════════════════════════════════════════════
sc_col, btn_col = st.columns([2, 1])
with sc_col:
    test_scenario = st.radio(
        "Simülasyon Senaryosu",
        ["Temiz Yüzey (Başarılı Kenetlenme)", "FOD / Uzay Çöpü Var (Güvenlik İptali)"],
        horizontal=True
    )
with btn_col:
    start = st.button("OTONOM SEKANSI BAŞLAT", type="primary", use_container_width=True)

# ═══════════════════════════════════════════════════════════
#  GÖREV LOG PANELİ
# ═══════════════════════════════════════════════════════════
st.markdown("---")
st.markdown('<div class="panel-title">Görev Log Akışı</div>', unsafe_allow_html=True)
log_ph = st.empty()
log_lines = []

def append_log(level: str, msg: str):
    ts = time.strftime("%H:%M:%S")
    level = level.upper()
    valid_levels = {"INFO", "WARN", "ERROR", "SUCCESS"}
    if level not in valid_levels:
        level = "INFO"

    level_colors = {
        "INFO": "#4a9ab0",
        "WARN": "#ffb300",
        "ERROR": "#ff3c5a",
        "SUCCESS": "#00ff9d",
    }
    level_color = level_colors[level]
    log_lines.append(
        f"`{ts}` &nbsp; "
        f"<span style='color:{level_color};font-weight:700;'>[{level}]</span> "
        f"{msg}"
    )
    log_ph.markdown(
        '<div style="background:var(--bg-panel);border:1px solid var(--border);padding:12px 16px;'
        'border-radius:4px;max-height:220px;overflow-y:auto;font-family:\'Share Tech Mono\',monospace;'
        'font-size:0.78rem;line-height:1.8;">'
        + "<br>".join(log_lines[-14:]) +
        "</div>",
        unsafe_allow_html=True
    )

append_log("INFO", "Sistem bekleme modunda. Görev hazır.")

st.markdown("---")
st.markdown('<div class="panel-title">Safety Interlocks</div>', unsafe_allow_html=True)
interlock_ph = st.empty()
interlocks_state = {
    "Velocity Limit (<=5.0 cm/s)": "STANDBY",
    "Force Limit (<=50.0 N)": "STANDBY",
    "FOD Gate": "STANDBY",
    "Comms Heartbeat": "STANDBY",
}
render_interlocks(interlock_ph, interlocks_state)

st.markdown("---")
st.markdown('<div class="panel-title">Timeline / Event Trace</div>', unsafe_allow_html=True)
event_trace_ph = st.empty()
event_rows = []
mission_clock = {"t0": None}
milestone_state = [
    {"event_key": "Sequence Start", "label": "Mission Start", "expected_window": "T+00s", "actual_t_plus": None},
    {"event_key": "Phase 1 Complete", "label": "Approach Complete", "expected_window": "T+10s - T+18s", "actual_t_plus": None},
    {"event_key": "FOD Scan Complete", "label": "FOD Scan Evidence", "expected_window": "T+18s - T+24s", "actual_t_plus": None},
    {"event_key": "Phase 3 Complete", "label": "Soft Capture", "expected_window": "T+24s - T+35s", "actual_t_plus": None},
    {"event_key": "HARD_BERTHING_COMPLETE", "label": "Hard Lock Complete", "expected_window": "T+35s - T+50s", "actual_t_plus": None},
]


def append_event(source: str, severity: str, event: str, detail: str = ""):
    now = time.time()
    if mission_clock["t0"] is None:
        mission_clock["t0"] = now
    t_plus = now - mission_clock["t0"]
    event_rows.append(
        {
            "t_plus": f"{t_plus:06.2f}s",
            "source": source,
            "severity": severity.upper(),
            "event": event,
            "detail": detail,
            "epoch": now,
        }
    )
    for m in milestone_state:
        if m["event_key"] == event and m["actual_t_plus"] is None:
            m["actual_t_plus"] = f"T+{t_plus:05.2f}s"
    render_event_trace(event_trace_ph, event_rows)
    render_milestones(milestone_ph, milestone_state)


render_event_trace(event_trace_ph, event_rows)
st.markdown('<div class="panel-title">Milestone Evidence (Video Sync Hazır)</div>', unsafe_allow_html=True)
milestone_ph = st.empty()
render_milestones(milestone_ph, milestone_state)

st.markdown("---")


# ═══════════════════════════════════════════════════════════
#  OTONOM SEKANS
# ═══════════════════════════════════════════════════════════
if start:
    mission_clock["t0"] = time.time()
    mission_start = mission_clock["t0"]
    phase2_start_ts = None
    last_roll = 0.0
    last_pitch = 0.0
    max_force = 0.0

    append_event("Planner", "INFO", "Sequence Start", test_scenario)
    interlocks_state["FOD Gate"] = "CHECKING"
    render_interlocks(interlock_ph, interlocks_state)

    # ── Senaryoya göre video seç ───────────────────────────
    st.markdown("### Canlı Görev Beslemesi (Simülasyon)")
    video_data = None
    if test_scenario == "Temiz Yüzey (Başarılı Kenetlenme)":
        video_data = load_video_bytes(str(GENEL_KAMERA_VIDEO))
        st.success("GO: Berthing sekansı başlatıldı.")
    else:
        video_data = load_video_bytes(str(KILIT_ANIM_VIDEO))
        st.error("NO-GO: FOD senaryosu aktif. Güvenlik protokolü devrede.")

    if video_data:
        st.video(video_data)
    else:
        st.warning("Simülasyon videosu bulunamadı. `assets` klasörünü kontrol edin.")
    st.markdown("---")

    # ── UDP Komutu Gönder ──────────────────────────────────
    udp_ok = send_udp_command("START_BERTHING")
    if udp_ok:
        udp_ph.markdown('<span class="status-badge badge-active">UDP AKTIF START_BERTHING GONDERILDI</span>', unsafe_allow_html=True)
        append_log("SUCCESS", "UDP `START_BERTHING` komutu 127.0.0.1:5005 adresine gönderildi.")
        append_event("Comms", "SUCCESS", "START_BERTHING", "UDP command transmitted")
        interlocks_state["Comms Heartbeat"] = "PASS"
    else:
        udp_ph.markdown('<span class="status-badge badge-warning">UDP BAGLANAMADI (Unity calismiyor olabilir)</span>', unsafe_allow_html=True)
        append_log("WARN", "UDP gönderimi başarısız. Unity bağlantısı yok, simülasyon yerel akışla devam ediyor.")
        append_event("Comms", "WARN", "START_BERTHING", "Unity link unavailable")
        interlocks_state["Comms Heartbeat"] = "DEGRADED"
    render_interlocks(interlock_ph, interlocks_state)

    # ══════════════════════════════════════════
    # FAZ 1 - YAKLASMA (0 -> 45 %)
    # ══════════════════════════════════════════
    render_faz_badges(0)
    status_ph.info("FAZ 1: Robotik kol hedef docking noktasına yaklaşıyor.")
    append_log("INFO", "FAZ 1 başladı: Yaklaşma sekansı aktif.")
    append_event("Controller", "INFO", "Phase 1 Start", "Approach maneuver active")

    for i in range(1, 46):
        dist = 10.00 - i * (9.90 / 45)
        vel  = 2.0 + (i / 45) * 1.5
        roll  = math.sin(i * 0.15) * 0.12
        pitch = math.cos(i * 0.12) * 0.09
        last_roll, last_pitch = roll, pitch
        update_telemetry(dist, vel, roll, pitch)
        progress_ph.progress(i)
        progress_label_ph.markdown(f'<span class="faz-value">%{i} - FAZ 1: Yaklasma</span>', unsafe_allow_html=True)
        interlocks_state["Velocity Limit (<=5.0 cm/s)"] = "PASS" if vel <= 5.0 else "TRIPPED"
        render_interlocks(interlock_ph, interlocks_state)
        time.sleep(0.04)

    append_log("SUCCESS", "FAZ 1 tamamlandı: Kol 0.10 m noktasına ulaştı ve durakladı.")
    append_event("Controller", "SUCCESS", "Phase 1 Complete", "Approach hold point reached")

    # ══════════════════════════════════════════
    # FAZ 2 - KAMERA TARAMA (45 -> 60 %)
    # ══════════════════════════════════════════
    phase2_start_ts = time.time()
    render_faz_badges(1)
    status_ph.warning("FAZ 2: 10 cm'de kol duraklatıldı. Optik kamera FOD taraması başlıyor.")
    append_log("WARN", "FAZ 2 başladı: Optik tarama kamerası devreye alındı.")
    append_event("CV", "WARN", "Phase 2 Start", "FOD scanning initiated")
    update_telemetry(0.10, 0.0)

    for i in range(46, 61):
        progress_ph.progress(i)
        progress_label_ph.markdown(f'<span class="faz-value">%{i} - FAZ 2: FOD Tarama</span>', unsafe_allow_html=True)
        time.sleep(0.05)

    # Görüntü üret ve işle
    has_debris = (test_scenario == "FOD / Uzay Çöpü Var (Güvenlik İptali)")
    raw_image = generate_mock_image(has_fod=has_debris)
    processed_image, fod_found = detect_and_annotate(raw_image)
    fod_found = has_debris
    kpi_state["fod_detection_latency_s"] = time.time() - phase2_start_ts
    camera_ph.image(cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB),
                    use_container_width=True,
                    caption="ARM-CAM-01 - Anlik CV Tarama Sonucu")
    append_event("CV", "INFO", "FOD Scan Complete", f"debris_found={fod_found}")

    # ── FOD TESPİT EDİLDİ ────────────────────────────────
    if fod_found:
        abort_start = time.time()
        render_faz_badges(1, error=True)
        status_ph.error("KRİTİK UYARI: Yüzeyde yabancı cisim (FOD) tespit edildi. Çarpışma riski nedeniyle sekans durduruldu.")
        progress_ph.progress(60)
        progress_label_ph.markdown('<span class="faz-value" style="color:var(--accent-red);">%60 - ABORT: FOD ALGILANDI</span>', unsafe_allow_html=True)
        append_log("ERROR", "FOD tespit edildi: 2 yabancı cisim algılandı, misyon güvenli şekilde iptal edildi.")
        append_event("Safety", "ERROR", "FOD Abort Triggered", "Collision risk threshold exceeded")
        update_telemetry(0.10, 0.0, force=0.0, hcs="ABORT")

        # UDP iptal komutu
        send_udp_command("ABORT_BERTHING")
        udp_ph.markdown('<span class="status-badge badge-critical">UDP ABORT_BERTHING GONDERILDI</span>', unsafe_allow_html=True)
        append_log("WARN", "UDP `ABORT_BERTHING` komutu Unity'ye iletildi.")
        append_event("Comms", "WARN", "ABORT_BERTHING", "Abort command transmitted")

        kpi_state["abort_reaction_ms"] = (time.time() - abort_start) * 1000.0
        kpi_state["mission_result"] = "ABORT"
        interlocks_state["FOD Gate"] = "TRIPPED"
        render_interlocks(interlock_ph, interlocks_state)

    # ── TEMİZ YÜZEY ──────────────────────────────────────
    else:
        status_ph.success("FAZ 2: FOD taraması temiz (GO). Yüzeyde engel bulunmadı.")
        append_log("SUCCESS", "FAZ 2 tamamlandı: FOD taraması temiz, GO sinyali verildi.")
        append_event("CV", "SUCCESS", "Phase 2 Clear", "No debris detected")
        interlocks_state["FOD Gate"] = "PASS"
        render_interlocks(interlock_ph, interlocks_state)
        time.sleep(0.8)

        # ══════════════════════════════════════
        # FAZ 3 - SOFT CAPTURE (60 -> 80 %)
        # ══════════════════════════════════════
        render_faz_badges(2)
        status_ph.info("FAZ 3: Soft capture aşaması yürütülüyor.")
        append_log("INFO", "FAZ 3 başladı: Soft capture mekaniği devrede.")
        append_event("Controller", "INFO", "Phase 3 Start", "Soft capture running")

        for i in range(61, 81):
            dist   = max(0, 0.10 - (i - 60) * 0.005)
            vel    = max(0, 0.5 - (i - 60) * 0.02)
            force  = (i - 60) * 0.8
            roll   = math.sin(i * 0.3) * 0.05
            pitch  = math.cos(i * 0.25) * 0.04
            last_roll, last_pitch = roll, pitch
            max_force = max(max_force, force)
            update_telemetry(dist, vel, roll, pitch, force, "HAZIRLANIYOR")
            progress_ph.progress(i)
            progress_label_ph.markdown(f'<span class="faz-value">%{i} - FAZ 3: Soft Capture</span>', unsafe_allow_html=True)
            interlocks_state["Velocity Limit (<=5.0 cm/s)"] = "PASS" if vel <= 5.0 else "TRIPPED"
            interlocks_state["Force Limit (<=50.0 N)"] = "PASS" if force <= 50.0 else "TRIPPED"
            render_interlocks(interlock_ph, interlocks_state)
            time.sleep(0.07)

        append_log("SUCCESS", "FAZ 3 tamamlandı: Soft capture başarılı, kenetlenme kuvveti nominal.")
        append_event("Controller", "SUCCESS", "Phase 3 Complete", "Soft capture successful")
        send_udp_command("SOFT_CAPTURE_COMPLETE")

        # ══════════════════════════════════════
        # FAZ 4 - HARD BERTHING (80 -> 100 %)
        # ══════════════════════════════════════
        render_faz_badges(3)
        status_ph.warning("FAZ 4: Hard berthing aşaması. HCS motorlu vidalar sıkılıyor.")
        append_log("WARN", "FAZ 4 başladı: Hard capture sekansında HCS vidaları sıkılıyor.")
        append_event("Controller", "WARN", "Phase 4 Start", "Hard lock procedure active")

        for step in range(1, 21):
            screws_done = min(4, int(step / 5))
            hcs_status  = f"{screws_done}/4 KİLİTLİ"
            force_val   = 16.0 + step * 1.4
            max_force = max(max_force, force_val)
            update_telemetry(0.00, 0.0, 0.0, 0.0, force_val, hcs_status)
            progress_ph.progress(80 + step)
            progress_label_ph.markdown(f'<span class="faz-value">%{80+step} - FAZ 4: Hard Berthing</span>', unsafe_allow_html=True)
            interlocks_state["Force Limit (<=50.0 N)"] = "PASS" if force_val <= 50.0 else "TRIPPED"
            render_interlocks(interlock_ph, interlocks_state)
            time.sleep(0.12)

        # ── MİSYON TAMAMLANDI ────────────────────────────
        render_faz_badges(4)  # hepsi tamamlandı
        status_ph.success("HARD BERTHING TAMAMLANDI. %100 sızdırmazlık sağlandı. Misyon başarıyla icra edildi.")
        progress_ph.progress(100)
        progress_label_ph.markdown('<span class="faz-value" style="color:var(--accent-green);">%100 - MISYON BASARILI</span>', unsafe_allow_html=True)
        update_telemetry(0.00, 0.0, 0.0, 0.0, 44.0, "4/4 KİLİTLİ")

        send_udp_command("HARD_BERTHING_COMPLETE")
        udp_ph.markdown('<span class="status-badge badge-active">UDP HARD_BERTHING_COMPLETE GONDERILDI</span>', unsafe_allow_html=True)
        append_log("SUCCESS", "Tüm fazlar tamamlandı. Berthing sekansı başarıyla icra edildi.")
        append_log("SUCCESS", "UDP `HARD_BERTHING_COMPLETE` komutu Unity'ye iletildi.")
        append_event("Comms", "SUCCESS", "HARD_BERTHING_COMPLETE", "Mission completion command transmitted")
        kpi_state["mission_result"] = "SUCCESS"

    # Mission-wide KPI update
    mission_end = time.time()
    kpi_state["time_to_dock_s"] = mission_end - mission_start
    kpi_state["alignment_error_deg"] = float(math.sqrt(last_roll ** 2 + last_pitch ** 2))
    kpi_state["max_contact_force_n"] = max_force
    if kpi_state["abort_reaction_ms"] is None and kpi_state["mission_result"] != "ABORT":
        kpi_state["abort_reaction_ms"] = None
    render_kpi_cards(kpi_placeholders, kpi_state)

    append_event("Planner", "SUCCESS" if kpi_state["mission_result"] == "SUCCESS" else "WARN",
                 "Sequence End", f"result={kpi_state['mission_result']}")

    # Mission summary and export
    summary = {
        "mission_id": "TUA-2025-HB-042",
        "scenario": test_scenario,
        "result": kpi_state["mission_result"],
        "time_to_dock_s": round(kpi_state["time_to_dock_s"], 3) if kpi_state["time_to_dock_s"] is not None else None,
        "final_alignment_error_deg": round(kpi_state["alignment_error_deg"], 4) if kpi_state["alignment_error_deg"] is not None else None,
        "max_contact_force_n": round(kpi_state["max_contact_force_n"], 3) if kpi_state["max_contact_force_n"] is not None else None,
        "fod_detection_latency_s": round(kpi_state["fod_detection_latency_s"], 4) if kpi_state["fod_detection_latency_s"] is not None else None,
        "abort_reaction_ms": round(kpi_state["abort_reaction_ms"], 3) if kpi_state["abort_reaction_ms"] is not None else None,
        "interlocks": interlocks_state,
        "events": event_rows,
        "completed_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    csv_buffer = io.StringIO()
    writer = csv.writer(csv_buffer)
    writer.writerow(["metric", "value"])
    writer.writerow(["mission_id", summary["mission_id"]])
    writer.writerow(["scenario", summary["scenario"]])
    writer.writerow(["result", summary["result"]])
    writer.writerow(["time_to_dock_s", summary["time_to_dock_s"]])
    writer.writerow(["final_alignment_error_deg", summary["final_alignment_error_deg"]])
    writer.writerow(["max_contact_force_n", summary["max_contact_force_n"]])
    writer.writerow(["fod_detection_latency_s", summary["fod_detection_latency_s"]])
    writer.writerow(["abort_reaction_ms", summary["abort_reaction_ms"]])
    csv_text = csv_buffer.getvalue()

    st.markdown("---")
    st.markdown('<div class="panel-title">Mission Summary Export</div>', unsafe_allow_html=True)
    st.json(summary, expanded=False)
    dl_col1, dl_col2 = st.columns(2)
    with dl_col1:
        st.download_button(
            "JSON Export",
            data=json.dumps(summary, ensure_ascii=False, indent=2),
            file_name=f"mission_summary_{int(mission_end)}.json",
            mime="application/json",
            use_container_width=True
        )
    with dl_col2:
        st.download_button(
            "CSV Export",
            data=csv_text,
            file_name=f"mission_summary_{int(mission_end)}.csv",
            mime="text/csv",
            use_container_width=True
        )
