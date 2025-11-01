from config.db import db, ma 

class MenuItem(db.Model):
    __tablename__ = 'menu_items'
    
    id_menu = db.Column(db.Integer, primary_key=True)
    name_menu = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50))
    image_url = db.Column(db.Text)
    is_available = db.Column(db.Boolean, default=True)

    order_items = db.relationship('OrderItem', back_populates='menu_item')

   