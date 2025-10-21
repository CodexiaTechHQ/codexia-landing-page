# 🌐 Codexia "Çok Yakında" Landing Page

Bu depo, Codexia'nın ana kurumsal web sitesi yayına girene kadar kullanılan, **güvenli ve profesyonel** "Çok Yakında" açılış sayfasının (Landing Page) kaynak kodunu içerir.

Bu sayfa, markamızın odağını (Siber Güvenlik, Yapay Zeka, Web Çözümleri) vurgulamak ve potansiyel müşterileri sosyal ve profesyonel kanallarımıza yönlendirmek amacıyla oluşturulmuştur.

## 🚀 Teknik Detaylar

Bu proje, basitliği ve hızlı dağıtımı (deployment) sağlamak için aşağıdaki teknolojilerle geliştirilmiştir:

* **Backend/Server:** **Python 3** ve **Flask** (Minimalist web çatısı)
* **Deployment:** **Render** (Ücretsiz plan ile sürekli dağıtım)
* **Web Sunucusu:** **Gunicorn** (Üretim ortamı için)
* **Frontend:** HTML5, CSS3, **Bootstrap 5** (Tasarım), Minimal **JavaScript** (Geri sayım sayacı için)

## 💾 Yerel Kurulum (Local Setup)

Bu projeyi yerel makinenizde çalıştırmak isterseniz:

1.  Depoyu klonlayın:
    ```bash
    git clone [REPO LİNKİ BURAYA GELECEK]
    cd codexia-landing-page
    ```
2.  Gerekli Python kütüphanelerini kurun:
    ```bash
    pip install -r requirements.txt
    ```
3.  Uygulamayı başlatın:
    ```bash
    python app.py
    ```
4.  Tarayıcınızda `http://127.0.0.1:5000` adresine giderek siteyi görüntüleyin.

## ☁️ Dağıtım (Deployment) Bilgisi

Uygulama, Render platformunda aşağıdaki komutlarla sürekli dağıtım (Continuous Deployment) kullanılarak yayınlanmaktadır:

* **Build Command:** `pip install -r requirements.txt`
* **Start Command:** `gunicorn app:app`

Her `main` dalına yapılan `git push` işlemi, Render tarafından otomatik olarak algılanır ve site güncellenir.

---

### 🔗 Faydalı Bağlantılar

* **Codexia Ana GitHub Organizasyonu:** https://github.com/CodexiaTechHQ
* **Web Güvenlik Kontrol Listemiz:** [Checklist Reposuna Link Gelecek]
