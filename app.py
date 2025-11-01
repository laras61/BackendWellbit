import os
from flask import Flask
from dotenv import load_dotenv

from config.db import db 
from config.extensions import bcrypt, jwt 

from models import user_model, order_model, menu_model, notification_model
from web import api 

# Load .env
load_dotenv()

app = Flask(__name__)

# ===========================
# Database
# ===========================
db_url = os.environ.get('DATABASE_URL')
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+psycopg2://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ===========================
# JWT
# ===========================
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

# ===========================
# Init extensions
# ===========================
db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)

# Register blueprint
app.register_blueprint(api) 

# Create tables (if not exists)
with app.app_context():
    db.create_all()

# Health check
@app.route("/")
def home():
    return {"status":"ok","message":"Backend ready 🚀"}

# Run lokal (optional)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
