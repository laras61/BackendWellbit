from config.db import db 

class Order(db.Model):
    __tablename__ = 'orders'
    
    id_order = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id_user'), nullable=False)
    status = db.Column(db.String(50), default='pending')
    delivery_address = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())

    user = db.relationship('User', back_populates='orders')

    items = db.relationship('OrderItem', back_populates='order', lazy=True, cascade="all, delete-orphan")

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id_order_item = db.Column(db.Integer, primary_key=True)
    id_order = db.Column(db.Integer, db.ForeignKey('orders.id_order'), nullable=False)
    id_menu_item = db.Column(db.Integer, db.ForeignKey('menu_items.id_menu'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False) 

    order = db.relationship('Order', back_populates='items')
    menu_item = db.relationship('MenuItem', back_populates='order_items')