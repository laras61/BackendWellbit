from flask import Blueprint

from controllers.menu_controller import get_all_menus, get_menu_by_id
from controllers.user_controller import register_user, login_user, get_user_profile
from controllers.order_controller import create_order, get_user_orders
from controllers.notification_controller import (
    get_user_notifications, 
    mark_notification_as_read, 
    mark_all_notifications_as_read
)

# 2. Buat satu Blueprint utama untuk semua API
api_bp = Blueprint('api_bp', __name__)

# --- User & Auth Routes ---
@api_bp.route('/api/auth/register', methods=['POST'])
def register_route():
    return register_user()

@api_bp.route('/api/auth/login', methods=['POST'])
def login_route():
    return login_user()

@api_bp.route('/api/profile', methods=['GET'])
def profile_route():
    return get_user_profile()

# --- Menu Routes ---
@api_bp.route('/api/menus', methods=['GET'])
def menus_route():
    return get_all_menus()

@api_bp.route('/api/menu/<int:menu_id>', methods=['GET'])
def menu_id_route(menu_id):
    return get_menu_by_id(menu_id)

# --- Order Routes ---
@api_bp.route('/api/orders', methods=['POST'])
def create_order_route():
    return create_order()

@api_bp.route('/api/orders', methods=['GET'])
def get_orders_route():
    return get_user_orders()

# --- Notification Routes ---
@api_bp.route('/api/notifications', methods=['GET'])
def get_notifications_route():
    return get_user_notifications()

@api_bp.route('/api/notifications/<int:notif_id>/read', methods=['PUT'])
def mark_one_read_route(notif_id):
    return mark_notification_as_read(notif_id)

@api_bp.route('/api/notifications/read-all', methods=['PUT'])
def mark_all_read_route():
    return mark_all_notifications_as_read()