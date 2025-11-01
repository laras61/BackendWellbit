from flask import jsonify, request
from config.db import db
from models.user_model import User 
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
import logging

# === 1. REGISTRASI ===
def register_user():
    """Membuat user baru (Registrasi) dengan password di-hash."""
    try:
        data = request.get_json()
        
        name = data['name_user']
        email = data['email']
        password_text = data['password']
        phone = data.get('phone_number')

        if not name or not email or not password_text:
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"status": "error", "message": "Email already registered"}), 400

        new_user = User(
            name_user=name,
            email=email,
            phone_number=phone
        )
        new_user.set_password(password_text)
        
        db.session.add(new_user)
        db.session.commit()
        
        result = {
            "id_user": new_user.id_user,
            "name_user": new_user.name_user,
            "email": new_user.email,
            "phone_number": new_user.phone_number,
            "created_at": new_user.created_at
        }
        
        return jsonify({
            "status": "success",
            "message": "User registered successfully",
            "data": result
        }), 201

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": "Database integrity error. Email might be taken."}), 400
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error in register_user: {e}")
        return jsonify({"status": "error", "message": f"An error occurred: {e}"}), 500

# === 2. LOGIN ===
def login_user():
    """Login user dan kembalikan JWT Token."""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"status": "error", "message": "Email and password are required"}), 400

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            access_token = create_access_token(identity=str(user.id_user))
            
            return jsonify({
                "status": "success",
                "message": "Login successful",
                "data": {
                    "access_token": access_token
                }
            }), 200
        else:
            return jsonify({"status": "error", "message": "Invalid email or password"}), 401

    except Exception as e:
        logging.error(f"Error in login_user: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# === 3. CEK PROFIL (TERPROTEKSI) ===
@jwt_required()
def get_user_profile():
    """Mengambil data profil user yang sedang login."""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"status": "error", "message": "User not found"}), 404
            
        result = {
            "id_user": user.id_user,
            "name_user": user.name_user,
            "email": user.email,
            "phone_number": user.phone_number,
            "created_at": user.created_at
        }
        
        return jsonify({
            "status": "success",
            "message": "Profile fetched successfully",
            "data": result
        }), 200
        
    except Exception as e:
        logging.error(f"Error in get_user_profile: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500