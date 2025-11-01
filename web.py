from flask import Blueprint

from controllers.menu_controller import get_all_menus, get_menu_by_id, create_menu, update_menu, delete_menu
from controllers.user_controller import register_user, login_user, get_user_profile
from controllers.order_controller import create_order, get_user_orders
from controllers.notification_controller import get_user_notifications, mark_notification_as_read, mark_all_notifications_as_read


api = Blueprint('api', __name__)

# --- User & Auth Routes ---
@api.route('/api/auth/register', methods=['POST'])
def register_route():
    return register_user()

@api.route('/api/auth/login', methods=['POST'])
def login_route():
    return login_user()

@api.route('/api/profile', methods=['GET'])
def profile_route():
    return get_user_profile()

# --- Menu Routes ---
@api.route('/api/menus', methods=['GET'])
def menus_route():
    return get_all_menus()

@api.route('/api/menu/<int:id_menu>', methods=['GET'])
def menu_id_route(id_menu):
    return get_menu_by_id(id_menu)

@api.route('/api/menu', methods=['POST'])
def create_menu_route():
    return create_menu()

@api.route('/api/menu/<int:id_menu>', methods=['PUT'])
def update_menu_route(id_menu):
    return update_menu(id_menu)

@api.route('/api/menu/<int:id_menu>', methods=['DELETE'])
def delete_menu_route(id_menu):
    return delete_menu(id_menu)

# --- Order Routes ---
@api.route('/api/orders', methods=['POST'])
def create_order_route():
    return create_order()

@api.route('/api/orders', methods=['GET'])
def get_orders_route():
    return get_user_orders()

# --- Notification Routes ---
@api.route('/api/notifications', methods=['GET'])
def get_notifications_route():
    return get_user_notifications()

@api.route('/api/notifications/<int:notif_id>/read', methods=['PUT'])
def mark_one_read_route(notif_id):
    return mark_notification_as_read(notif_id)

@api.route('/api/notifications/read-all', methods=['PUT'])
def mark_all_read_route():
    return mark_all_notifications_as_read()