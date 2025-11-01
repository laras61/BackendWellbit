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
    """Membuat pesanan baru dari user yang sedang login."""
    try:
        current_user_id = get_jwt_identity()
        
        data = request.get_json()
        
        item_list = data.get('items')
        delivery_address = data.get('delivery_address')

        if not item_list or not delivery_address:
            return jsonify({"status": "error", "message": "Missing items or delivery address"}), 400

        total_price = 0
        order_items_to_create = []
        menu_names = [] 

        for item in item_list:
            menu_id = item.get('id_menu')
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

        # --- Jika semua item valid, buat pesanan ---
        
        # 1. Buat 'Order' (induknya)
        new_order = Order(
            id_user=current_user_id,
            total_price=total_price,
            delivery_address=delivery_address,
            status='pending' 
        )

        new_order.items.extend(order_items_to_create)

        notif_message = f"Pesanan Anda untuk {', '.join(menu_names)} telah diterima! Total: Rp {total_price}"
        new_notification = Notification(
            id_user=current_user_id,
            message=notif_message,
            type='activity' # Tipe 'activity' untuk pesanan
        )

        # 4. Simpan semuanya ke database
        db.session.add(new_order)
        db.session.add(new_notification)
        db.session.commit()
        
        # Siapkan data balikan (tanpa schema)
        result = {
            "id_order": new_order.id_order,
            "id_user": new_order.id_user,
            "total_price": new_order.total_price,
            "status": new_order.status,
            "delivery_address": new_order.delivery_address,
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
        
        # Ambil semua order milik user tsb, urutkan dari yg terbaru
        orders = Order.query.filter_by(id_user=current_user_id).order_by(Order.created_at.desc()).all()

        if not orders:
            return jsonify({"status": "success", "message": "You have no orders yet", "data": []}), 200
        
        # Ubah jadi list dictionary
        result = []
        for order in orders:
            result.append({
                "id_order": order.id_order,
                "status": order.status,
                "delivery_address": order.delivery_address,
                "created_at": order.created_at,
                "items": [
                    {
                        "id_menu_item": oi.id_menu_item,
                        "quantity": oi.quantity,
                        "price": oi.price,
                        # Kita tambahkan info nama menu agar gampang
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