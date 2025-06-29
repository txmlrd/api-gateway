from flask import Blueprint, session, jsonify, request
from app.extensions import jwt_required, get_jwt_identity
from security.check_device import check_device_token
import requests
from app.config import Config
from security.check_permission import check_permission
from security.role_required import role_required
from werkzeug.utils import secure_filename

role_permission_bp = Blueprint('role_permission', __name__)

############# ROLE Endpoint #############
@role_permission_bp.route('/role/list', methods=['GET'])
@jwt_required()
@check_device_token
@role_required(['admin'])
# @check_permission('manage_role')
def role_list():
  try:
    response = requests.get(f"{Config.ROLE_SERVICE_URL}/role/list",)
    return jsonify(response.json()), response.status_code
  except requests.RequestException as e:
    return jsonify({"error": "Role Management Service unavailable", "details": str(e)}), 500
  
@role_permission_bp.route('/role/create', methods=['POST'])
@jwt_required()
@check_device_token
@role_required(['admin'])
# @check_permission('manage_role')
def create_role():
  data = request.get_json()
  if not data:
    return jsonify({"error": "No data provided"}), 400
  try:
    response = requests.post(f"{Config.ROLE_SERVICE_URL}/role/create", json=data)
    return jsonify(response.json()), response.status_code
  except requests.RequestException as e:
    return jsonify({"error": "Role Management Service unavailable", "details": str(e)}), 500

@role_permission_bp.route('/role/delete/<id>', methods=['DELETE'])
@jwt_required()
@check_device_token
@role_required(['admin'])
# @check_permission('manage_role')
def delete_role(id):
  try:
    response = requests.delete(f"{Config.ROLE_SERVICE_URL}/role/delete/{id}",)
    return jsonify(response.json()), response.status_code
  except requests.RequestException as e:
    return jsonify({"error": "Role Management Service unavailable", "details": str(e)}), 500

@role_permission_bp.route('/role/update/<id>', methods=['PUT'])
@jwt_required()
@check_device_token
@role_required(['admin'])
# @check_permission('manage_role')
def update_role(id):
  data = request.get_json()
  if not data:
    return jsonify({"error": "No data provided"}), 400
  try:
    response = requests.put(f"{Config.ROLE_SERVICE_URL}/role/update/{id}", json=data)
    return jsonify(response.json()), response.status_code
  except requests.RequestException as e:
    return jsonify({"error": "Role Management Service unavailable", "details": str(e)}), 500
  
@role_permission_bp.route('/role/assign-permission', methods=['POST'])
@jwt_required()
@check_device_token
@role_required(['admin'])
# @check_permission('manage_role')
def assign_permission():
  data = request.get_json()
  if not data:
    return jsonify({"error": "No data provided"}), 400
  try:
    response = requests.post(f"{Config.ROLE_SERVICE_URL}/role/assign-permission", json=data)
    return jsonify(response.json()), response.status_code
  except requests.RequestException as e:
    return jsonify({"error": "Role Management Service unavailable", "details": str(e)}), 500
  
############################# PERMISSiON Endpoint #############################  

@role_permission_bp.route('/permission/list', methods=['GET'])
@jwt_required()
@check_device_token
@role_required(['admin'])
# @check_permission('manage_role')
def permission_list():
  try:
    response = requests.get(f"{Config.ROLE_SERVICE_URL}/permission/list",)
    return jsonify(response.json()), response.status_code
  except requests.RequestException as e:
    return jsonify({"error": "Role Management Service unavailable", "details": str(e)}), 500
  
@role_permission_bp.route('/permission/create', methods=['POST'])
@jwt_required()
@check_device_token
@role_required(['admin'])
# @check_permission('manage_role')
def create_permission():
  data = request.get_json()
  if not data:
    return jsonify({"error": "No data provided"}), 400
  try:
    response = requests.post(f"{Config.ROLE_SERVICE_URL}/permission/create", json=data)
    return jsonify(response.json()), response.status_code
  except requests.RequestException as e:
    return jsonify({"error": "Role Management Service unavailable", "details": str(e)}), 500

@role_permission_bp.route('/permission/delete/<id>', methods=['DELETE'])
@jwt_required()
@check_device_token
@role_required(['admin'])
# @check_permission('manage_role')
def delete_permission(id):
  try:
    response = requests.delete(f"{Config.ROLE_SERVICE_URL}/permission/delete/{id}",)
    return jsonify(response.json()), response.status_code
  except requests.RequestException as e:
    return jsonify({"error": "Role Management Service unavailable", "details": str(e)}), 500

@role_permission_bp.route('/permission/update/<id>', methods=['PUT'])
@jwt_required()
@check_device_token
@role_required(['admin'])
# @check_permission('manage_role')
def update_permission(id):
  data = request.get_json()
  if not data:
    return jsonify({"error": "No data provided"}), 400
  try:
    response = requests.put(f"{Config.ROLE_SERVICE_URL}/permission/update/{id}", json=data)
    return jsonify(response.json()), response.status_code
  except requests.RequestException as e:
    return jsonify({"error": "Role Management Service unavailable", "details": str(e)}), 500