from config.db import db, ma # type: ignore

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id_notif = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(20), default='info')
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())

    user = db.relationship('User', back_populates='notifications')
