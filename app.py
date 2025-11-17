from flask import Flask, render_template, request, redirect, url_for, flash, session
import os # Ortam değişkenlerini okumak için eklendi

app = Flask(__name__)

# --- GÜVENLİK AYARLARI VE ORTAM DEĞİŞKENLERİ ---
# Güvenlik, oturumlar ve flash mesajları için zorunludur.
# 'SECRET_KEY' ortam değişkeninden oku, yoksa yedek değer kullan.
app.secret_key = os.environ.get('SECRET_KEY', 'cok_gizli_ve_uzun_bir_sifre_buraya_gelecek_12345') 

# Admin kimlik bilgileri ortam değişkenlerinden okunur.
# os.environ.get() ile bu değerler doğrudan Python dosyasında sabit kodlanmaktan kurtulur.
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin') # Yedek değer 'admin'
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'codexia_master') # Yedek değer 'codexia_master'

# --- ROTLAR ---

@app.route('/')
def index():
    # Ana sayfa
    return render_template('index.html')

# --- İLETİŞİM FORMU ROTASI ---
@app.route('/api/contact', methods=['POST'])
def handle_contact_form():
    name = request.form.get('name')
    email = request.form.get('email')
    service = request.form.get('service')
    # message değişkeni alınırken hata yok, sadece düzenlenmiş kısmı dahil ettim.
    
    flash(f'Yeni Teklif Talebi alındı! İlgili Alan: {service}. Gönderen: {name}', 'success')
    
    return redirect(url_for('index'))

# --- ADMIN GİRİŞ ROTASI ---
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            flash('Giriş başarılı!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Hatalı kullanıcı adı veya şifre.', 'error')
            
    if session.get('logged_in'):
        return redirect(url_for('admin_dashboard'))
            
    return render_template('admin_login.html')

# --- ADMIN DASHBOARD ROTASI ---
@app.route('/admin/dashboard')
def admin_dashboard():
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
    # Yerel çalıştırmada debug modunu kullanır
    app.run(debug=True)
