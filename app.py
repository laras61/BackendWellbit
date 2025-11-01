import os
from flask import Flask
from dotenv import load_dotenv

from config.db import db 
from config.extensions import bcrypt, jwt 

from models import user_model, order_model, menu_model, notification_model

from web import api 

load_dotenv()

app = Flask(__name__)

db_url = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

jwt_key = os.environ.get('JWT_SECRET_KEY')
app.config['JWT_SECRET_KEY'] = jwt_key

db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)

app.register_blueprint(api) 

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)