# Peran: Ruang Mekanikal
# Tugas: File ini menyiapkan koneksi database (SQLAlchemy) dan
# alat bantu 'packaging' (Marshmallow) agar bisa dipakai di file lain.

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Kita buat objek kosong dulu
db = SQLAlchemy()
ma = Marshmallow()

