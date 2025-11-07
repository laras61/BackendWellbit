from flask import jsonify, request
from config.db import db
from models.user_model import User
from models.menu_model import MenuItem
from models.order_model import Order, OrderItem
from models.notification_model import Notification 
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

# === 1. MEMBUAT PESANAN BARU (PROTECTED) ===
@jwt_required()
def create_order():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        item_list = data.get('items')

        if not item_list:
            return jsonify({"status": "error", "message": "Missing items data"}), 400

        total_price = 0
        order_items_to_create = []
        menu_names = [] 

        for item in item_list:
            menu_id = item.get('id_menu_item') 
            quantity = item.get('quantity')
            
            if not menu_id or not quantity or quantity <= 0:
                return jsonify({"status": "error", "message": "Invalid item data"}), 400

            menu = MenuItem.query.get(menu_id)
            
            if not menu:
                return jsonify({"status": "error", "message": f"Menu with id {menu_id} not found"}), 404
            
            if not menu.is_available:
                return jsonify({"status": "error", "message": f"{menu.name_menu} is not available"}), 400

            current_item_price = menu.price * quantity
            total_price += current_item_price
            
            order_item = OrderItem(
                id_menu_item=menu_id,
                quantity=quantity,
                price=menu.price 
            )
            order_items_to_create.append(order_item)
            menu_names.append(menu.name_menu)

        
        # 1. Buat 'Order' (induknya)
        new_order = Order(
            id_user=current_user_id,
            status='pending' 
        )

        # 2. Tambahkan semua item ke order
        new_order.items.extend(order_items_to_create)

        # 3. Buat notifikasi
        notif_message = f"Pesanan Anda untuk {', '.join(menu_names)} telah diterima! Total: Rp {total_price}"
        new_notification = Notification(
            id_user=current_user_id,
            message=notif_message,
            type='activity'
        )

        # 4. Simpan semuanya ke database
        db.session.add(new_order)
        db.session.add(new_notification)
        db.session.commit()
        
        # Siapkan data balikan (tanpa schema)
        result = {
            "id_order": new_order.id_order,
            "id_user": new_order.id_user,
            "total_price": new_order.total_price, # Memanggil properti @property
            "status": new_order.status,
            "created_at": new_order.created_at,
            "items": [
                {
                    "id_menu_item": oi.id_menu_item,
                    "quantity": oi.quantity,
                    "price": oi.price
                } for oi in new_order.items
            ]
        }

        return jsonify({
            "status": "success",
            "message": "Order created successfully",
            "data": result
        }), 201

    except Exception as e:
        db.session.rollback()
        logging.error(f"Error in create_order: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# === 2. MELIHAT RIWAYAT PESANAN (PROTECTED) ===
@jwt_required()
def get_user_orders():
    """Mengambil semua riwayat pesanan dari user yang sedang login."""
    try:
        current_user_id = get_jwt_identity()
        
        orders = Order.query.filter_by(id_user=current_user_id).order_by(Order.created_at.desc()).all()

        if not orders:
            return jsonify({"status": "success", "message": "You have no orders yet", "data": []}), 200
        
        result = []
        for order in orders:
            result.append({
                "id_order": order.id_order,
                "status": order.status,
                "created_at": order.created_at,
                "total_price": order.total_price, # Memanggil properti @property
                "items": [
                    {
                        "id_menu_item": oi.id_menu_item,
                        "quantity": oi.quantity,
                        "price": oi.price,
                        "name_menu": oi.menu_item.name_menu if oi.menu_item else "Menu not found"
                    } for oi in order.items
                ]
            })

        return jsonify({
            "status": "success",
            "message": "Orders fetched successfully",
            "data": result
        }), 200

    except Exception as e:
        logging.error(f"Error in get_user_orders: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500