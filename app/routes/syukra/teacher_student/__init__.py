from flask import Blueprint, request, jsonify, url_for, render_template
from extensions import  jwt_required
from datetime import datetime, timedelta
import requests
from werkzeug.utils import secure_filename
from config import Config
from security.check_device import check_device_token
from security.check_permission import check_permission

syukra_teacher_student_bp = Blueprint('syukra-teacher-student', __name__)

@syukra_teacher_student_bp.route('/public/user/class/', methods=['GET'])
@jwt_required()
@check_device_token
@check_permission('view_class')
def get_class():
    try:
        response = requests.get(
            f"{Config.URL_CLASS_CONTROL}/public/user/class",
            params=request.args
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Class Control Service unavailable", "details": str(e)}), 503

@syukra_teacher_student_bp.route('/public/assessment/upcoming/', methods=['GET'])
@jwt_required()
@check_device_token
@check_permission('view_assessment')
def get_upcoming_assessments():
    try:
        response = requests.get(
            f"{Config.URL_CLASS_CONTROL}/public/assessment/upcoming",
            params=request.args
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Assessment Service unavailable", "details": str(e)}), 503