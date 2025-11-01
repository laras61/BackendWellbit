from config.extensions import bcrypt
from config.db import db, ma 

class User(db.Model):
    __tablename__ = 'users' 
    
    id_user = db.Column(db.Integer, primary_key=True)
    name_user = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())
   
    orders = db.relationship('Order', back_populates='user', lazy=True)
    notifications = db.relationship('Notification', back_populates='user', lazy=True)

    def set_password(self, password_text):
        """Membuat ash password dari plain text"""
        self.password = bcrypt.generate_password_hash(password_text).decode('utf-8')

    def check_password(self, password_text):
        """Mengecek plain text password dengan hash di database"""
        return bcrypt.check_password_hash(self.password, password_text)

