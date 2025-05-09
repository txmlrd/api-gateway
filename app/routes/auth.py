from flask import Blueprint, jsonify, request
import requests
from config import Config
from extensions import jwt_required, get_jwt_identity, decode_token, redis_client, get_jwt
from security.check_device import check_device_token
auth_bp = Blueprint('api_gateway', __name__)

@auth_bp.route('/login-face', methods=['POST'])
def login_face():
    try:
        # Ambil data dan file dari request asli
        form_data = request.form
        files = [('face_image', file) for file in request.files.getlist('face_image')]

        # Kirim form dan file ke User Service
        response = requests.post(
            f"{Config.AUTH_SERVICE_URL}/login-face",
            data=form_data,
            files=files
        )
        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "User Service unavailable", "details": str(e)}), 503


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.form 
    try:
        response = requests.post(
            f"{Config.AUTH_SERVICE_URL}/login",
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

@auth_bp.route('/logout', methods=['GET'])
@jwt_required()
@check_device_token
def logout():
    token = request.headers.get('Authorization').split(' ')[1]
    user_id = get_jwt_identity()
    jti = get_jwt()["jti"]
    try:    
        response = requests.get(f"{Config.AUTH_SERVICE_URL}/logout", headers={"Authorization": f"Bearer {token}"})
        if response.status_code == 200:
            # Blacklist token dan hapus dari Redis
            redis_client.setex(f"blacklist_{jti}", 3600, 'blacklisted')
            redis_client.delete(f"user_active_token:{user_id}")
            return jsonify({"msg": "Logout successful"}), 200
        return jsonify({"error": "Logout failed"}), 400
    except Exception as e:
        return jsonify({"error": "Auth service unreachable", "details": str(e)}), 500
            

