from flask import Blueprint, request, jsonify, url_for, render_template
from extensions import  jwt_required
from datetime import datetime, timedelta
import requests
from werkzeug.utils import secure_filename
from config import Config
from security.check_device import check_device_token
from security.check_permission import check_permission

syukra_student_bp = Blueprint('syukra-student', __name__)

######################## ASSESSMENT SESSION ########################
@syukra_student_bp.route('/answer', methods=['POST'])
@jwt_required()
@check_device_token
@check_permission('assessment_session')
def post_answer_student():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400
    try:
        response = requests.post(
            f"{Config.URL}/answer",
            json=data,
            headers={"Authorization": request.headers.get("Authorization")}
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Assessment Service unavailable", "details": str(e)}), 503

@syukra_student_bp.route('/submission/submit/', methods=['POST'])
@jwt_required()
@check_device_token
@check_permission('assessment_session')
def submit_submission():
    try:
        response = requests.post(
            f"{Config.URL}/submission/submit", params=request.args,
            headers={"Authorization": request.headers.get("Authorization")}
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Assessment Service unavailable", "details": str(e)}), 503

########################## ASSESSMENT DETAIL STUDENT ########################
@syukra_student_bp.route('/student/assessment/', methods=['GET'])
@jwt_required()
@check_device_token
@check_permission('assessment_detail_student')
def get_assessment_by_id_userid():
    try:
        response = requests.get(
            f"{Config.URL}/student/assessment",
            params=request.args,
            headers={"Authorization": request.headers.get("Authorization")}
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Assessment Service unavailable", "details": str(e)}), 503
      
@syukra_student_bp.route('/submission', methods=['POST'])
@jwt_required()
@check_device_token
@check_permission('assessment_detail_student')
def start_submission():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400
    try:
        response = requests.post(
            f"{Config.URL}/submission",
            json=data,
            headers={"Authorization": request.headers.get("Authorization")}
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Assessment Service unavailable", "details": str(e)}), 503

@syukra_student_bp.route('/answer/submission/', methods=['GET'])
@jwt_required()
@check_device_token
@check_permission('assessment_detail_student')
def get_answer_by_submission_id():
    try:
        response = requests.get(
            f"{Config.URL}/answer/submission",
            params=request.args,
            headers={"Authorization": request.headers.get("Authorization")}
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Assessment Service unavailable", "details": str(e)}), 503

############################ ASSIGNMENT DETAIL STUDENT ########################
@syukra_student_bp.route('/student/kelas/assignment/', methods=['GET'])
@jwt_required()
@check_device_token
@check_permission('assignment_detail_student')
def get_assignment_by_id():
    try:
        response = requests.get(
            f"{Config.URL_CLASS_CONTROL}/student/kelas/assignment",
            params=request.args,
            headers={"Authorization": request.headers.get("Authorization")}
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Assignment Service unavailable", "details": str(e)}), 503


@syukra_student_bp.route('/student-assignment/', methods=['POST'])
@jwt_required()
@check_device_token
@check_permission('assignment_detail_student')
def upload_file_submission():
    file =request.files.get('file')
    try:

        response = requests.post(
            f"{Config.URL_CONTENT}/student-assignment",
            params=request.args,
            files=file,
            headers={"Authorization": request.headers.get("Authorization")}
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Assignment Service unavailable", "details": str(e)}), 503

@syukra_student_bp.route('/student-assignment/<uuid>', methods=['DELETE'])
@jwt_required()
@check_device_token
@check_permission('assignment_detail_student')
def delete_student_assignment(uuid):
    try:
        response = requests.delete(
            f"{Config.URL_CONTENT}/student-assignment/{uuid}",
            headers={"Authorization": request.headers.get("Authorization")}
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Assignment Service unavailable", "details": str(e)}), 503

@syukra_student_bp.route('/student/kelas/assignment-submission', methods=['POST'])
@jwt_required()
@check_device_token
@check_permission('assignment_detail_student')
def create_assignment_submission():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400
    try:
        response = requests.post(
            f"{Config.URL_CLASS_CONTROL}/student/kelas/assignment-submission",
            json=data,
            headers={"Authorization": request.headers.get("Authorization")}
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Assignment Service unavailable", "details": str(e)}), 503
      
@syukra_student_bp.route('/student-assignment/user', methods=['GET'])
@jwt_required()
@check_device_token
@check_permission('assignment_detail_student')
def get_student_uploaded_file():
    try:
        response = requests.get(
            f"{Config.URL_CONTENT}/student-assignment/user",
            params=request.args,
            headers={"Authorization": request.headers.get("Authorization")}
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Assignment Service unavailable", "details": str(e)}), 503
        
############################## CLASS STUDENT TAB ########################
@syukra_student_bp.route('/student/assessment/class/', methods=['GET'])
@jwt_required()
@check_device_token
@check_permission('class_student_tab')
def get_assessment_by_classid_userid():
    try:
        response = requests.get(
            f"{Config.URL}/student/assessment/class",
            params=request.args,
            headers={"Authorization": request.headers.get("Authorization")}
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Class Service unavailable", "details": str(e)}), 503
    
@syukra_student_bp.route('/student/public/class/members/', methods=['GET'])
@jwt_required()
@check_device_token
@check_permission('class_student_tab')
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

@syukra_student_bp.route('/student/kelas/weekly-section/class/', methods=['GET'])
@jwt_required()
@check_device_token
@check_permission('class_student_tab')
def get_weekly_section_by_classid():
    try:
        response = requests.get(
            f"{Config.URL_CLASS_CONTROL}/kelas/weekly-section/class",
            params=request.args,
            headers={"Authorization": request.headers.get("Authorization")}
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Class Service unavailable", "details": str(e)}), 503
    
@syukra_student_bp.route('/student/item-pembelajaran/<uuid>', methods=['GET'])
@jwt_required()
@check_device_token
@check_permission('class_student_tab')
def get_item_pembelajaran_by_uuid_student(uuid):
    try:
        response = requests.get(
            f"{Config.URL_CONTENT}/item-pembelajaran/{uuid}",
            headers={"Authorization": request.headers.get("Authorization")}
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Item Pembelajaran Service unavailable", "details": str(e)}), 503

