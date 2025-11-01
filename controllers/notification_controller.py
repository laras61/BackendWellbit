from flask import jsonify, request
from config.db import db
from models.notification_model import Notification
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

# === 1. MENGAMBIL SEMUA NOTIFIKASI USER ===
@jwt_required()
def get_user_notifications():
    """Mengambil semua notifikasi untuk user yang sedang login."""
    try:
        current_user_id_str = get_jwt_identity()
        current_user_id = int(current_user_id_str)

        notifications = Notification.query.filter_by(id_user=current_user_id).order_by(Notification.created_at.desc()).all()

        if not notifications:
            return jsonify({"status": "success", "message": "You have no notifications", "data": []}), 200

        result = []
        for notif in notifications:
            result.append({
                "id_notif": notif.id_notif,
                "message": notif.message,
                "type": notif.type,
                "is_read": notif.is_read,
                "created_at": notif.created_at
            })
        
        return jsonify({
            "status": "success",
            "message": "Notifications fetched successfully",
            "data": result
        }), 200

    except Exception as e:
        logging.error(f"Error in get_user_notifications: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# === 2. MENANDAI SATU NOTIFIKASI SEBAGAI 'READ' ===
@jwt_required()
def mark_notification_as_read(notif_id):
    """Menandai satu notifikasi sebagai 'read' berdasarkan ID-nya."""
    try:
        current_user_id = int(get_jwt_identity())
        
        # Cari notifikasinya
        notification = Notification.query.get(notif_id)

        if not notification:
            return jsonify({"status": "error", "message": "Notification not found"}), 404
        
        # CEK KEAMANAN: Pastikan user ini pemilik notifikasi tersebut
        if notification.id_user != current_user_id:
            return jsonify({"status": "error", "message": "Unauthorized"}), 403 # 403 Forbidden

        # Jika sudah dibaca, tidak perlu update
        if notification.is_read:
            return jsonify({"status": "success", "message": "Notification was already marked as read"}), 200

        # Update status
        notification.is_read = True
        db.session.commit()
        
        return jsonify({"status": "success", "message": "Notification marked as read"}), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Error in mark_notification_as_read: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# === 3. MENANDAI SEMUA NOTIFIKASI SEBAGAI 'READ' ===
@jwt_required()
def mark_all_notifications_as_read():
    """Menandai semua notifikasi milik user sebagai 'read'."""
    try:
        current_user_id = int(get_jwt_identity())

        # Cari semua notifikasi user ini yang 'is_read == False'
        unread_notifications = Notification.query.filter_by(
            id_user=current_user_id, 
            is_read=False
        ).all()

        if not unread_notifications:
            return jsonify({"status": "success", "message": "No unread notifications to mark"}), 200

        # Update semua yang belum dibaca
        for notif in unread_notifications:
            notif.is_read = True
        
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": f"Successfully marked {len(unread_notifications)} notifications as read."
        }), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Error in mark_all_notifications_as_read: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500