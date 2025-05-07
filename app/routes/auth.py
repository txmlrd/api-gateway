from flask import Blueprint, jsonify, request
import requests
from config import Config
from extensions import jwt_required, get_jwt_identity, decode_token, redis_client
from security.check_device import check_device_token
auth_bp = Blueprint('api_gateway', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.form 
    try:
        response = requests.post(
            f"{Config.USER_SERVICE_URL}/login",
            data=data,
            timeout=5
        )
    except Exception as e:
        return jsonify({"error": "Auth service unreachable", "details": str(e)}), 500

    if response.status_code == 200:
        result = response.json()
        access_token = result['access_token']
        
        try:
            decoded = decode_token(access_token)
            jti = decoded['jti']
            user_id = decoded['sub']  # karena identity=user.id
            redis_client.setex(f"user_active_token:{user_id}", 3600, jti)
        except Exception as e:
            return jsonify({"error": "Token decoding failed", "details": str(e)}), 500

        return jsonify(access_token=access_token), 200

    return jsonify({"error": "Login failed"}), 401

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
@check_device_token
def profile():
    token = request.headers.get('Authorization').split(' ')[1]
    response = requests.get(f"{Config.USER_SERVICE_URL}/profile", headers={"Authorization": f"Bearer {token}"})
    if response.status_code == 200:
        return jsonify(response.json()), 200
    return jsonify({"error": "Failed to fetch profile"}), 400

@auth_bp.route('/logout', methods=['GET'])
@jwt_required()
@check_device_token
def logout():
    token = request.headers.get('Authorization').split(' ')[1]
    try:
        response = requests.get(f"{Config.USER_SERVICE_URL}/logout", headers={"Authorization": f"Bearer {token}"})
        if response.status_code == 200:
            # Hapus token dari Redis
            user_id = response
            redis_client.delete(f"user_active_token:{user_id}")
            
            return jsonify({"msg": "Logout successful"}), 200
        return jsonify({"error": "Logout failed"}), 400
    except Exception as e:
        return jsonify({"error": "Auth service unreachable", "details": str(e)}), 500
            

