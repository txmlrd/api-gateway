from flask import Blueprint, request, jsonify, url_for, render_template
from extensions import  jwt_required
from datetime import datetime, timedelta
import requests
from werkzeug.utils import secure_filename
from config import Config
from security.check_device import check_device_token
from security.check_permission import check_permission
from flask import Response
from flask import request

syukra_admin_bp = Blueprint('syukra-admin', __name__)

@syukra_admin_bp.route('/kelas/admin', methods=['POST'])
@jwt_required()
@check_device_token
@check_permission('class_control')
def create_class():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400
    
    try:
        response = requests.post(f"{Config.URL_CLASS_CONTROL}/kelas/admin", json=data)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Class Control Service unavailable", "details": str(e)}), 503

@syukra_admin_bp.route('/member/admin', methods=['POST'])
@jwt_required()
@check_device_token
@check_permission('class_control')
def add_member_class():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400
    
    try:
        response = requests.post(f"{Config.URL_CLASS_CONTROL}/member/admin", json=data)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Class Control Service unavailable", "details": str(e)}), 503

@syukra_admin_bp.route('/kelas/admin/', methods=['DELETE'])
@jwt_required()
@check_device_token
@check_permission('class_control')
def delete_class():
    try:
        response = requests.delete(
            f"{Config.URL_CLASS_CONTROL}/kelas/admin",
            params=request.args
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Class Control Service unavailable", "details": str(e)}), 503

@syukra_admin_bp.route('/kelas/admin', methods=['GET'])
@jwt_required()
@check_device_token
@check_permission('class_control')
def get_all_classes_paginated():
    try:
        response = requests.get(f"{Config.URL_CLASS_CONTROL}/kelas/admin", params=request.args)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Class Control Service unavailable", "details": str(e)}), 503

@syukra_admin_bp.route('/kelas/admin/', methods=['PUT'])
@jwt_required()
@check_device_token
@check_permission('class_control')
def update_class():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400
    
    try:
        response = requests.put(f"{Config.URL_CLASS_CONTROL}/kelas/admin",params=request.args, json=data)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Class Control Service unavailable", "details": str(e)}), 503