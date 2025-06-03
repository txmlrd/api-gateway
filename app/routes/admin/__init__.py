from flask import Blueprint, request, jsonify, url_for, render_template
from extensions import  jwt_required
from datetime import datetime, timedelta
import requests
from werkzeug.utils import secure_filename
from config import Config
from security.check_device import check_device_token
from security.check_permission import check_permission
from security.check_crucial_token import check_crucial_token

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/get-user', methods=['GET'])
@jwt_required()
@check_device_token
@check_permission('manage_user')
def get_all_user():
    try:
        response = requests.get(f"{Config.USER_SERVICE_URL}/admin/get-user",params=request.args, headers={"Authorization": f"{request.headers['Authorization']}"})
        if response.status_code == 200:
            return jsonify(response.json()), 200
        return jsonify(response.json()), 400
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "User Service unavailable", "details": str(e)}), 503

@admin_bp.route('/search-user', methods=['GET'])
@jwt_required()
@check_device_token
@check_permission('manage_user')
def search_user():
    try:
        response = requests.get(f"{Config.USER_SERVICE_URL}/admin/search-user",params=request.args, headers={"Authorization": f"{request.headers['Authorization']}"})
        if response.status_code == 200:
            return jsonify(response.json()), 200
        return jsonify(response.json()), 400
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "User Service unavailable", "details": str(e)}), 503
      
@admin_bp.route('/modify-role', methods=['POST'])
@jwt_required()
@check_device_token
@check_permission('manage_user')
@check_crucial_token()
def modify_role():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400
    try:
        response = requests.post(f"{Config.USER_SERVICE_URL}/admin/modify-role", json=data, headers={"Authorization": f"{request.headers['Authorization']}"})
        if response.status_code == 200:
            return jsonify(response.json()), 200
        return jsonify(response.json()), 400
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "User Service unavailable", "details": str(e)}), 503
      
@admin_bp.route('/delete-user/<uuid>', methods=['DELETE'])
@jwt_required()
@check_device_token
@check_permission('manage_user')
@check_crucial_token()
def delete_user(uuid):
    try:
        response = requests.delete(
            f"{Config.USER_SERVICE_URL}/admin/delete-user/{uuid}",
            headers={"Authorization": request.headers.get("Authorization")}
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "User Service unavailable", "details": str(e)}), 503
    
@admin_bp.route('/inject-crucial-token', methods=['POST'])
@jwt_required()
@check_device_token
@check_permission('manage_user')
def inject_crucial_token():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400
    try:
        response = requests.post(f"{Config.AUTH_SERVICE_URL}/inject-crucial-token", json=data, headers={"Authorization": f"{request.headers['Authorization']}"})
        if response.status_code == 200:
            return jsonify(response.json()), 200
        return jsonify(response.json()), 400
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "User Service unavailable", "details": str(e)}), 503
    
@admin_bp.route('/delete-crucial-token', methods=['DELETE'])
@jwt_required()
@check_device_token
@check_permission('manage_user')
def delete_crucial_token():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400
    try:
        response = requests.delete(
            f"{Config.AUTH_SERVICE_URL}/delete-crucial-token",
            json=data,
            headers={"Authorization": request.headers.get("Authorization")}
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "User Service unavailable", "details": str(e)}), 503
    
@admin_bp.route('/verify-email-user', methods=['POST'])
@jwt_required()
@check_device_token
@check_permission('manage_user')
def verify_email_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400
    try:
        response = requests.post(f"{Config.USER_SERVICE_URL}/admin/verify-email-user", json=data, headers={"Authorization": f"{request.headers['Authorization']}"})
        if response.status_code == 200:
            return jsonify(response.json()), 200
        return jsonify(response.json()), 400
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "User Service unavailable", "details": str(e)}), 503