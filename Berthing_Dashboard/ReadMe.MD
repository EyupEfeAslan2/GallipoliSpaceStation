# Gallipoli Space Station - Otonom Görev Kontrol ve Yanaştırma Sistemi (Berthing Dashboard)

Bu depo (repository), Gallipoli Uzay İstasyonu projemizin otonom yanaştırma (berthing), yabancı madde tespiti (FOD) ve yörünge savunma sistemlerinin simüle edildiği, izlendiği ve yönetildiği merkezi web arayüzünü içermektedir.

Sistem, geleneksel manuel astronot operasyonlarını ortadan kaldırarak; uzay arayüzlerinde sıfır hata toleranslı, yapay zeka ve görüntü işleme destekli bir Tam Otonom Görev Kontrol mimarisi sunar.

## Temel Özellikler

* Tam Otonom Yanaştırma (Berthing) Simülasyonu: IDSS (Uluslararası Kenetlenme Sistemi Standardı) Metot 1'e tam uyumlu, "Çift Sarkaç" (Double-Rocker) mekanizmamızın logaritmik hız kesme algoritmalarıyla hizalanma ve kilitlenme süreçlerinin canlı veri simülasyonu.
* Yapay Zeka Destekli FOD Tespiti: Sızdırmazlık yüzeylerindeki tehlikeli yabancı maddeleri (FOD) tespit etmek için entegre edilmiş OpenCV tabanlı görüntü işleme algoritması. Tespit edilen anomaliler sistem üzerinden anlık olarak JSON veya CSV formatında dışa aktarılabilir.
* Yörünge Savunma Sistemi (WARDEN & ELVO): Mikro-meteor ve uzay çöpü tehditlerine karşı istasyonun otonom reaksiyonlarını (lazerle imha ve otonom kaçınma manevraları) içeren savunma modülü simülasyonları.
* Dinamik Kullanıcı Arayüzü: Node, Life, Core ve Research modüllerimizin yüksek çözünürlüklü CAD tasarımlarını ve genel istasyon mimarisini barındıran, modüller arası kolay geçiş sağlayan interaktif web platformu.

## Kullanılan Teknolojiler

* Arayüz (Frontend/Backend): Python, Streamlit
* Görüntü İşleme: OpenCV, NumPy, Pandas
* Veri Yönetimi: JSON, CSV Export modülleri
* Mekanik Tasarım Kaynağı: SolidWorks (CAD entegrasyonu ve animasyonlar)

## Dosya Yapısı

```bash
GallipoliSpaceStation/
│
└── Berthing_Dashboard/         # Ana uygulama klasörü
    ├── assets/                 # CAD görselleri, simülasyon videoları ve arayüz ikonları
    ├── pages/                  # Simülasyon alt sayfaları (FOD_Tespiti.py, Savunma.py vb.)
    ├── Home.py                 # Uygulamanın ana giriş noktası (İstasyon Mimarisi)
    ├── nav.py                  # Yan menü (Sidebar) navigasyon komponenti
    ├── requirements.txt        # Proje bağımlılıkları (Python kütüphaneleri)
    └── .gitignore

    Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin:

1. Depoyu Klonlayın:

Bash
git clone [https://github.com/EyupeEfeAslan2/GallipoliSpaceStation.git](https://github.com/EyupeEfeAslan2/GallipoliSpaceStation.git)
cd GallipoliSpaceStation/Berthing_Dashboard
2. Gerekli Kütüphaneleri Yükleyin:
Sanal bir ortam (virtual environment) oluşturmanız tavsiye edilir.

Bash
pip install -r requirements.txt
3. Uygulamayı Başlatın:

Bash
streamlit run Home.py
Uygulama başarıyla başlatıldığında http://localhost:8501 adresinden Görev Kontrol paneline erişebilirsiniz.

Bu proje, yeni nesil uzay istasyonu mimarilerinde otonom sistem entegrasyonunu kanıtlamak amacıyla geliştirilmiştir.

Ayrıca https://eyupefeaslan2-gallipolispacestati-berthing-dashboardhome-g5gide.streamlit.app/ adresinden de canlı olarak erişebilirsiniz.