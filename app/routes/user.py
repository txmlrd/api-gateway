from flask import Blueprint, session, jsonify, request
from extensions import jwt_required, get_jwt_identity
from security.check_device import check_device_token
import requests
from config import Config

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
@check_device_token
def profile():
    token = request.headers.get('Authorization').split(' ')[1]
    response = requests.get(f"{Config.USER_SERVICE_URL}/profile", headers={"Authorization": f"Bearer {token}"})
    if response.status_code == 200:
        return jsonify(response.json()), 200
    return jsonify({"error": "Failed to fetch profile"}), 400

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.form
    try:
        response = requests.post(f"{Config.USER_SERVICE_URL}/register", data=data, timeout=5)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "User Service unavailable", "details": str(e)}), 503
    
@user_bp.route('/update', methods=['POST'])
@jwt_required()
@check_device_token
def update_profile():
    token = request.headers.get('Authorization').split(' ')[1]
    data = request.form
    try:
        response = requests.post(f"{Config.USER_SERVICE_URL}/update", headers={"Authorization": f"Bearer {token}"}, data=data, timeout=5)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "User Service unavailable", "details": str(e)}), 503

@user_bp.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
@check_device_token
def delete_profile(id):
    token = request.headers.get('Authorization').split(' ')[1]
    try:
        response = requests.delete(f"{Config.USER_SERVICE_URL}/delete/{id}", headers={"Authorization": f"Bearer {token}"}, timeout=5)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "User Service unavailable", "details": str(e)}), 503
    
@user_bp.route('/reset-password/request', methods=['POST'])
def reset_password_request():
    data = request.form
    try:
        response = requests.post(f"{Config.USER_SERVICE_URL}/reset-password/request", data=data, timeout=5)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "User Service unavailable", "details": str(e)}), 503