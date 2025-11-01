from models.menu_model import MenuItem
from config.db import db 
from flask import jsonify, request

def get_all_menus():
    """Mengambil semua menu."""
    try:
        all_menus = MenuItem.query.all()
        
        result = []
        for menu in all_menus:
            result.append({
                "id_menu": menu.id_menu,
                "name_menu": menu.name_menu,
                "description": menu.description,
                "price": menu.price,
                "category": menu.category,
                "image_url": menu.image_url,
                "is_available": menu.is_available
            })
        
        return jsonify({
            "status": "success",
            "message": "Menus fetched successfully",
            "data": result
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

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

# Di sini Anda bisa tambahkan:
# def create_menu(): ... (Untuk POST)
# def update_menu(menu_id): ... (Untuk PUT)
# def delete_menu(menu_id): ... (Untuk DELETE)