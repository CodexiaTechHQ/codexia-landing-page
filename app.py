from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os 

# --- UYGULAMA VE VERİTABANI KONFİGÜRASYONU ---
app = Flask(__name__)

# Şifreler ve anahtar ortam değişkenlerinden okunur
app.secret_key = os.environ.get('SECRET_KEY', 'cok_gizli_ve_uzun_bir_sifre_buraya_gelecek_12345') 
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin') 
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'codexia_master') 

# SQLite veritabanı dosyasının konumu: Uygulama kök dizininde site.db
# Not: Canlı ortamda SQLite yerine PostgreSQL kullanmak daha güvenli ve ölçeklenebilirdir.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- VERİTABANI MODELİ: Teklif Talepleri ---
class ContactRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    service = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"ContactRequest('{self.name}', '{self.email}')"

# 🔥 DÜZELTME: db.create_all() Gunicorn tarafından da çalıştırılması için buraya taşındı.
# Bu kod, uygulama nesnesi oluşturulduktan hemen sonra çalışır ve tabloları oluşturur.
with app.app_context():
    db.create_all()

# --- ROTLAR ---

@app.route('/')
def index():
    return render_template('index.html')

# --- İLETİŞİM FORMU ROTASI (Veriyi Kalıcı Olarak Kaydeder) ---
@app.route('/api/contact', methods=['POST'])
def handle_contact_form():
    name = request.form.get('name')
    email = request.form.get('email')
    service = request.form.get('service')
    message = request.form.get('message')
    
    new_request = ContactRequest(
        name=name,
        email=email,
        service=service,
        message=message
    )
    
    db.session.add(new_request)
    db.session.commit()
    
    flash(f'Yeni Teklif Talebi başarıyla alındı. En kısa sürede size dönüş yapacağız!', 'success')
    
    return redirect(url_for('index'))

# --- ADMIN GİRİŞ ROTASI ---
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            flash('Admin Paneline Giriş başarılı!', 'success') 
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Hatalı kullanıcı adı veya şifre.', 'error') 
            
    if session.get('logged_in'):
        return redirect(url_for('admin_dashboard'))
            
    return render_template('admin_login.html')

# --- ADMIN DASHBOARD ROTASI (Veritabanından Mesajları Çeker) ---
@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('logged_in'):
        flash('Bu sayfaya erişmek için giriş yapmalısınız.', 'error')
        return redirect(url_for('admin_login'))
    
    requests = ContactRequest.query.order_by(ContactRequest.timestamp.desc()).all()
    
    return render_template('admin_dashboard.html', requests=requests)

# --- ÇIKIŞ ROTASI ---
@app.route('/admin/logout')
def admin_logout():
    session.pop('logged_in', None)
    flash('Başarıyla çıkış yaptınız.', 'success')
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    # Yerel çalıştırma (debug modu)
    app.run(debug=True)
