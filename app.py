from flask import Flask, jsonify
from config.db import db, ma
from config.extensions import bcrypt, jwt
from models import user_model, order_model, menu_model, notification_model
from web import api

app = Flask(__name__)

# Database (hardcode)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:OLLHpNbSjDrUHxtcRGJQJpQGlDeyOZj@turntable.proxy.rlwy.net:48535/railway"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# JWT secret (hardcode)
app.config['JWT_SECRET_KEY'] = "super-secret-random-string-12345!@#$%"

# Init extensions
db.init_app(app)
ma.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)

# Register blueprint
app.register_blueprint(api)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return jsonify({"status":"ok","message":"Backend ready 🚀"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
