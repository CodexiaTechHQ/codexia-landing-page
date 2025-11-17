from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # templates/index.html dosyasını çağırır
    return render_template('index.html')
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
# Gizli anahtar: Güvenlik, oturumlar ve flash mesajları için zorunludur.
app.secret_key = 'cok_gizli_ve_uzun_bir_sifre_buraya_gelecek_12345' 

# Örnek ve basit kullanıcı doğrulama verileri (Gerçek uygulamada veritabanından okunur)
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'codexia_master'

@app.route('/')
def index():
    # Ana sayfa
    return render_template('index.html')

# --- İLETİŞİM FORMU ROTASI (Index'teki "Teklif Talep Et" butonu buraya POST yapacak) ---
@app.route('/api/contact', methods=['POST'])
def handle_contact_form():
    # Normalde burada form verileri veritabanına kaydedilir veya e-posta gönderilir.
    
    # Kullanıcıdan gelen form verilerini al
    name = request.form.get('name')
    email = request.form.get('email')
    service = request.form.get('service')
    message = request.form.get('message')
    
    # (Sadece Örnek) Veriyi kaydettikten sonra, adminin görmesi için ona bir mesaj gösterelim.
    flash(f'Yeni Teklif Talebi alındı! İlgili Alan: {service}. Gönderen: {name}', 'success')
    
    # Form gönderimi başarılı olduktan sonra kullanıcıyı ana sayfaya geri yönlendir.
    return redirect(url_for('index'))


# --- ADMIN GİRİŞ ROTASI ---
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            # Başarılı giriş: Oturum başlatılır.
            session['logged_in'] = True
            flash('Giriş başarılı!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Hatalı kullanıcı adı veya şifre.', 'error')
            
    # Giriş yapılmışsa, direkt dashboard'a yönlendir.
    if session.get('logged_in'):
         return redirect(url_for('admin_dashboard'))
            
    return render_template('admin_login.html')

# --- ADMIN DASHBOARD ROTASI ---
@app.route('/admin/dashboard')
def admin_dashboard():
    # Eğer kullanıcı giriş yapmamışsa, giriş sayfasına yönlendir.
    if not session.get('logged_in'):
        flash('Bu sayfaya erişmek için giriş yapmalısınız.', 'error')
        return redirect(url_for('admin_login'))
        
    return render_template('admin_dashboard.html')

# --- ÇIKIŞ ROTASI ---
@app.route('/admin/logout')
def admin_logout():
    session.pop('logged_in', None)
    flash('Başarıyla çıkış yaptınız.', 'success')
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    # Render'da çalışırken bu kısım devreye girmez, gunicorn kullanılır.
    # debug=True, geliştirme aşamasında faydalıdır.
    app.run(debug=True)
if __name__ == '__main__':
    # Basit bir sunucu ile uygulamayı başlatır (Render'da bu otomatik yapılır)

    app.run(debug=True)
