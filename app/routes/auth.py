from flask import Blueprint, jsonify, request
import requests
from config import Config
from extensions import jwt_required, get_jwt_identity, decode_token, redis_client, get_jwt
from security.check_device import check_device_token
auth_bp = Blueprint('api_gateway', __name__)

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
@check_device_token  # opsional, kalau kamu pakai
def refresh_token_gateway():
    token = request.headers.get("Authorization")

    try:
        response = requests.post(
            f"{Config.AUTH_SERVICE_URL}/refresh",
            headers={"Authorization": token}
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Auth Service unavailable",
            "details": str(e)
        }), 503

@auth_bp.route('/login-face', methods=['POST'])
def login_face():
    try:
        # Ambil data dan file dari request asli
        form_data = request.form
        files = [('face_image', file) for file in request.files.getlist('face_image')]

        # Kirim form dan file ke Auth Service
        response = requests.post(
            f"{Config.AUTH_SERVICE_URL}/login-face",
            data=form_data,
            files=files,
        )

        if response.status_code == 200:
            result = response.json()
            access_token = result['access_token']
            refresh_token = result['refresh_token']

            try:
                decoded = decode_token(access_token)
                jti = decoded['jti']
                user_id = decoded['sub']  # identity=user.id
                redis_client.setex(f"user_active_token:{user_id}", 3600, jti)
            except Exception as e:
                return jsonify({"error": "Token decoding failed", "details": str(e)}), 500

            response = {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "verification_result": result
            }
            return jsonify(response), 200

        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Auth Service unavailable", "details": str(e)}), 503



@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400 
    try:
        response = requests.post(
            f"{Config.AUTH_SERVICE_URL}/login",
            json=data,
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

        return jsonify(result), 200
    
    result = response.json()
    return jsonify(result), response.status_code


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
        response = response.json()
        return jsonify(response), response.status_code
    except Exception as e:
        return jsonify({"error": "Auth service unreachable", "details": str(e)}), 500
    
@auth_bp.route('/crucial-verify', methods=['POST'])
@jwt_required()
@check_device_token
def crucial_verify():
    token = request.headers.get('Authorization').split(' ')[1]
    data = request.form
    files = [('image', file) for file in request.files.getlist('image')]
    if not data or not files:
        return jsonify({"error": "Invalid input"}), 400
    try:
        response = requests.post(f"{Config.AUTH_SERVICE_URL}/crucial-verify", headers={"Authorization": f"Bearer {token}"}, data=data, files=files)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Auth Service unavailable", "details": str(e)}), 503
