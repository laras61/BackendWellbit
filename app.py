import os
from flask import Flask
from dotenv import load_dotenv

# 1. Import library config
from config.db import db 
from config.extensions import bcrypt, jwt 

# 2. IMPORT SEMUA MODEL (Urutan ini tetap penting)
from models import user_model, order_model, menu_model, notification_model

# 3. IMPORT SATU BLUEPRINT DARI web.py
from web import api_bp # <--- INI PERUBAHANNYA

# 4. Muat .env
load_dotenv()

# 5. Buat aplikasi Flask
app = Flask(__name__)

# 6. Konfigurasi Database & JWT
db_url = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

jwt_key = os.environ.get('JWT_SECRET_KEY')
app.config['JWT_SECRET_KEY'] = jwt_key

# 7. Hubungkan ekstensi dengan 'app'
db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)

# 8. Daftarkan SATU Blueprint
app.register_blueprint(api_bp) # <--- INI PERUBAHANNYA

# 9. Buat tabel
with app.app_context():
    db.create_all()

# 10. Jalankan server
if __name__ == '__main__':
    app.run(debug=True)