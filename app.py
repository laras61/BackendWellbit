from flask import Flask, jsonify
from config.db import db
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

from config.db import db, ma
from config.extensions import bcrypt, jwt

CORS(app)  

db.init_app(app)
ma.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)
migrate = Migrate(app, db)

from web import api
app.register_blueprint(api)


with app.app_context():
    from models import user_model, order_model, menu_model, notification_model
    db.create_all()

@app.route("/")
def home():
    return jsonify({"status":"ok","message":"Backend ready 🚀"})

port = int(os.environ.get('PORT', 5000))

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=port)