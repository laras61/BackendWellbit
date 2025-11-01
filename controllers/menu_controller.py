from models.menu_model import MenuItem
from config.db import db 
from flask import jsonify, request

# ============================================================
# GET - Ambil Semua Menu
# ============================================================
def get_all_menus():
    """Mengambil semua menu."""
    try:
        all_menus = MenuItem.query.all()
        result = [{
            "id_menu": menu.id_menu,
            "name_menu": menu.name_menu,
            "description": menu.description,
            "price": menu.price,
            "category": menu.category,
            "image_url": menu.image_url,
            "is_available": menu.is_available
        } for menu in all_menus]
        
        return jsonify({
            "status": "success",
            "message": "Menus fetched successfully",
            "data": result
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ============================================================
# GET - Ambil Menu Berdasarkan ID
# ============================================================
def get_menu_by_id(menu_id):
    """Mengambil satu menu berdasarkan ID."""
    try:
        menu = MenuItem.query.get(menu_id)
        if not menu:
            return jsonify({"status": "error", "message": "Menu not found"}), 404
        
        result = {
            "id_menu": menu.id_menu,
            "name_menu": menu.name_menu,
            "description": menu.description,
            "price": menu.price,
            "category": menu.category,
            "image_url": menu.image_url,
            "is_available": menu.is_available
        }
        
        return jsonify({
            "status": "success",
            "message": "Menu fetched successfully",
            "data": result
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ============================================================
# POST - Tambah Menu Baru
# ============================================================
def create_menu():
    """Menambahkan menu baru."""
    try:
        data = request.get_json()

        # Validasi input sederhana
        if not data.get("name_menu") or not data.get("price"):
            return jsonify({"status": "error", "message": "name_menu and price are required"}), 400
        
        new_menu = MenuItem(
            name_menu=data.get("name_menu"),
            description=data.get("description"),
            price=data.get("price"),
            category=data.get("category"),
            image_url=data.get("image_url"),
            is_available=data.get("is_available", True)
        )

        db.session.add(new_menu)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Menu created successfully",
            "data": {
                "id_menu": new_menu.id_menu,
                "name_menu": new_menu.name_menu,
                "price": new_menu.price
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


# ============================================================
# PUT - Update Menu
# ============================================================
def update_menu(menu_id):
    """Memperbarui data menu."""
    try:
        menu = MenuItem.query.get(menu_id)
        if not menu:
            return jsonify({"status": "error", "message": "Menu not found"}), 404

        data = request.get_json()

        menu.name_menu = data.get("name_menu", menu.name_menu)
        menu.description = data.get("description", menu.description)
        menu.price = data.get("price", menu.price)
        menu.category = data.get("category", menu.category)
        menu.image_url = data.get("image_url", menu.image_url)
        menu.is_available = data.get("is_available", menu.is_available)

        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Menu updated successfully",
            "data": {
                "id_menu": menu.id_menu,
                "name_menu": menu.name_menu,
                "price": menu.price
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


# ============================================================
# DELETE - Hapus Menu
# ============================================================
def delete_menu(menu_id):
    """Menghapus menu berdasarkan ID."""
    try:
        menu = MenuItem.query.get(menu_id)
        if not menu:
            return jsonify({"status": "error", "message": "Menu not found"}), 404

        db.session.delete(menu)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Menu deleted successfully"
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
