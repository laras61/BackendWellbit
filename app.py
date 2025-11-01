from flask import Flask, jsonify
import os
from config.db import db, ma
from config.extensions import bcrypt, jwt
from models import user_model, order_model, menu_model, notification_model
from web import api
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Gunakan environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# JWT secret dari environment
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

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
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host="0.0.0.0", port=port)