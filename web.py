from flask import Blueprint
from controllers.menu_controller import get_all_menus, get_menu_by_id, create_menu, update_menu, delete_menu
from controllers.user_controller import register_user, login_user, get_user_profile
from controllers.order_controller import create_order, get_user_orders
from controllers.notification_controller import (
    get_user_notifications, 
    mark_notification_as_read, 
    mark_all_notifications_as_read
)

api = Blueprint('api', __name__)

# User & Auth
api.route('/api/auth/register', methods=['POST'])(register_user)
api.route('/api/auth/login', methods=['POST'])(login_user)
api.route('/api/profile', methods=['GET'])(get_user_profile)

# Menu
api.route('/api/menus', methods=['GET'])(get_all_menus)
api.route('/api/menu/<int:menu_id>', methods=['GET'])(get_menu_by_id)

# Order
api.route('/api/orders', methods=['POST'])(create_order)
api.route('/api/orders', methods=['GET'])(get_user_orders)

# Notification
api.route('/api/notifications', methods=['GET'])(get_user_notifications)
api.route('/api/notifications/<int:notif_id>/read', methods=['PUT'])(mark_notification_as_read)
api.route('/api/notifications/read-all', methods=['PUT'])(mark_all_notifications_as_read)
