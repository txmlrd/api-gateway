from flask import Blueprint, request, jsonify, url_for, render_template
from extensions import  jwt_required
from datetime import datetime, timedelta
import requests
from werkzeug.utils import secure_filename
from config import Config
from security.check_device import check_device_token
from security.role_required import role_required
from security.check_permission import check_permission
from flask import Response

syukra_teacher_student_bp = Blueprint('syukra-teacher-student', __name__)

@syukra_teacher_student_bp.route('/public/user/class/', methods=['GET'])
@jwt_required()
@check_device_token
@role_required(['admin', 'teacher', 'student'])
# @check_permission('view_class')
def get_class():
    try:
        response = requests.get(
            f"{Config.URL_CLASS_CONTROL}/public/user/class",
            params=request.args,
            headers={"Authorization": request.headers.get("Authorization")}
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Class Control Service unavailable", "details": str(e)}), 503

@syukra_teacher_student_bp.route('/public/assessment/upcoming/', methods=['GET'])
@jwt_required()
@check_device_token
@role_required(['admin', 'teacher', 'student'])
@check_permission('view_assessment')
def get_upcoming_assessments():
    try:
        response = requests.get(
            f"{Config.URL_CLASS_CONTROL}/public/assessment/upcoming",
            params=request.args,
            headers={"Authorization": request.headers.get("Authorization")}
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Assessment Service unavailable", "details": str(e)}), 503


@syukra_teacher_student_bp.route('/item-pembelajaran/', methods=['GET'])
@jwt_required()
@check_device_token
@role_required(['admin', 'teacher', 'student'])
@check_permission('get_item_pembelajaran')
def get_item_pembelajaran_by_uuid():
    try:
        response = requests.get(f"{Config.URL_CONTENT}/item-pembelajaran", params=request.args, stream=True, headers={"Authorization": request.headers.get("Authorization")})
        
        return Response(
            response.iter_content(chunk_size=1024),
            content_type=response.headers.get('Content-Type'),
            status=response.status_code,
            headers=dict(response.headers)
        )
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Class Service unavailable", "details": str(e)}), 503

@syukra_teacher_student_bp.route('/public/class/members/', methods=['GET'])
@jwt_required()
@check_device_token
@role_required(['admin', 'teacher', 'student'])
@check_permission('class_teacher_student')
def get_class_members_student():
    try:
        response = requests.get(
            f"{Config.URL_CLASS_CONTROL}/public/class/members",
            params=request.args,
            headers={"Authorization": request.headers.get("Authorization")}
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Class Service unavailable", "details": str(e)}), 503

@syukra_teacher_student_bp.route('/kelas', methods=['GET'])
@jwt_required()
@check_device_token
@role_required(['admin', 'teacher', 'student'])
@check_permission('class_teacher_student')
def get_class_detail_by_id():
    try:
        response = requests.get(f"{Config.URL_CLASS_CONTROL}/kelas", params=request.args, headers={"Authorization": request.headers.get("Authorization")})
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Class Control Service unavailable", "details": str(e)}), 503