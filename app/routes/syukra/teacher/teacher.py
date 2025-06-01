from flask import Blueprint, request, jsonify, url_for, render_template
from extensions import  jwt_required
from datetime import datetime, timedelta
import requests
from werkzeug.utils import secure_filename
from config import Config
from security.check_device import check_device_token
from security.check_permission import check_permission
from flask import Response

syukra_teacher_bp = Blueprint('syukra-teacher', __name__)

####################### MODIFY ASSESMENT ########################
@syukra_teacher_bp.route('/teacher/assessment/update', methods=['PUT'])
@jwt_required()
@check_device_token
@check_permission('modify_assessment')
def update_assessment():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400
    
    try:
        response = requests.get(f"{Config.URL}/teacher/assessment/update",json=data)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Class Service unavailable", "details": str(e)}), 503

@syukra_teacher_bp.route('/teacher/assessment/delete', methods=['DELETE'])
@jwt_required()
@check_device_token
@check_permission('modify_assessment')
def delete_assessment():
    try:
        response = requests.delete(f"{Config.URL}/teacher/assessment/delete",params=request.args)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Class Service unavailable", "details": str(e)}), 503


####################### MODIFY QUESTION ########################
@syukra_teacher_bp.route('/assessment/question/update', methods=['PUT'])
@jwt_required()
@check_device_token
@check_permission('modify_question')
def update_questions_choices():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400
      
    try:
        response = requests.put(f"{Config.URL}/assessment/question/update", json=data)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Class Service unavailable", "details": str(e)}), 503

####################### ASSESSMENT DETAIL - TEACHER ########################
@syukra_teacher_bp.route('/teacher/assessment/', methods=['GET'])
@jwt_required()
@check_device_token
@check_permission('assessment_detail_teacher')
def get_assessment_detail_by_id():
    try:
        response = requests.get(f"{Config.URL}/teacher/assessment", params=request.args)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Class Service unavailable", "details": str(e)}), 503

@syukra_teacher_bp.route('/assement/submission/', methods=['GET'])
@jwt_required()
@check_device_token
@check_permission('assessment_detail_teacher')
def get_student_submission_by_assesment_id():
    try:
        response = requests.get(f"{Config.URL}/assement/submission", params=request.args)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Class Service unavailable", "details": str(e)}), 503

@syukra_teacher_bp.route('/assessment/detail/questions/', methods=['GET'])
@jwt_required()
@check_device_token
@check_permission('assessment_detail_teacher')
def get_questions_by_assessment_id():
    try:
        response = requests.get(f"{Config.URL}/assessment/detail/questions/", params=request.args)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Class Service unavailable", "details": str(e)}), 503
      
@syukra_teacher_bp.route('/assessment/question/', methods=['GET'])
@jwt_required()
@check_device_token
@check_permission('assessment_detail_teacher')
def get_questions_by_id():
    try:
        response = requests.get(f"{Config.URL}/assessment/question", params=request.args)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Class Service unavailable", "details": str(e)}), 503

@syukra_teacher_bp.route('/assessment/question/', methods=['DELETE'])
@jwt_required()
@check_device_token
@check_permission('assessment_detail_teacher')
def delete_questions_by_id():
    try:
        response = requests.delete(f"{Config.URL}/assessment/question", params=request.args)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Class Service unavailable", "details": str(e)}), 503

@syukra_teacher_bp.route('/assessment/submission/', methods=['DELETE'])
@jwt_required()
@check_device_token
@check_permission('assessment_detail_teacher')
def delete_submission_by_id():
    try:
        response = requests.delete(f"{Config.URL}/assement/submission", params=request.args)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Class Service unavailable", "details": str(e)}), 503
      
######################### CREATE ASSESSMENT ########################
@syukra_teacher_bp.route('/teacher/assessment', methods=['POST'])
@jwt_required()
@check_device_token
@check_permission('create_assessment')
def create_assessment():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400
    
    try:
        response = requests.post(f"{Config.URL}/teacher/assessment", json=data)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Class Service unavailable", "details": str(e)}), 503

@syukra_teacher_bp.route('/assessment/question', methods=['POST'])
@jwt_required()
@check_device_token
@check_permission('create_assessment')
def create_questions():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400
    
    try:
        response = requests.post(f"{Config.URL}/assessment/question", json=data)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Class Service unavailable", "details": str(e)}), 503

######################### ASSIGNMENT DETAIL ########################
@syukra_teacher_bp.route('/teacher/kelas/assignment/', methods=['GET'])
@jwt_required()
@check_device_token
@check_permission('assignment_detail_teacher')
def get_assignment_detail_by_id():
    try:
        response = requests.get(f"{Config.URL_CLASS_CONTROL}/teacher/kelas/assignment", params=request.args)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Class Control Service unavailable", "details": str(e)}), 503

@syukra_teacher_bp.route('/kelas/assignment-submission', methods=['GET'])
@jwt_required()
@check_device_token
@check_permission('assignment_detail_teacher')
def get_submission_by_assignment_id():
    try:
        response = requests.get(f"{Config.URL_CLASS_CONTROL}/kelas/assignment-submission", params=request.args)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Class Control Service unavailable", "details": str(e)}), 503

@syukra_teacher_bp.route('/kelas/assignment-submission/student', methods=['GET'])
@jwt_required()
@check_device_token
@check_permission('assignment_detail_teacher')
def get_submission_by_id():
    try:
        response = requests.get(f"{Config.URL_CLASS_CONTROL}/kelas/assignment-submission/student", params=request.args)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Class Control Service unavailable", "details": str(e)}), 503
      
@syukra_teacher_bp.route('/kelas/assignment-submission', methods=['DELETE'])
@jwt_required()
@check_device_token
@check_permission('assignment_detail_teacher')
def delete_submission_by_submission_id():
    try:
        response = requests.delete(f"{Config.URL_CLASS_CONTROL}/kelas/assignment-submission", params=request.args)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Class Control Service unavailable", "details": str(e)}), 503

@syukra_teacher_bp.route('/kelas/assignment-submission', methods=['PUT'])
@jwt_required()
@check_device_token
@check_permission('assignment_detail_teacher')
def update_score():
    try:
        response = requests.put(f"{Config.URL_CLASS_CONTROL}/kelas/assignment-submission", params=request.args)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Class Control Service unavailable", "details": str(e)}), 503
      
@syukra_teacher_bp.route('/teacher/student-assignment/<uuid>', methods=['GET'])
@jwt_required()
@check_device_token
@check_permission('assignment_detail_teacher')
def get_submission_by_uuid(uuid):
    try:
        response = requests.get(f"{Config.URL_CONTENT}/teacher/student-assignment/{uuid}")
        return Response(
            response.iter_content(chunk_size=1024),
            content_type=response.headers.get('Content-Type'),
            status=response.status_code,
            headers=dict(response.headers)
        )
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Class Control Service unavailable", "details": str(e)}), 503

########################### CLASS STUDENT TAB ########################
@syukra_teacher_bp.route('/public/class/members/', methods=['GET'])
@jwt_required()
@check_device_token
@check_permission('class_student_tab_teacher')
def get_class_members():
    try:
        response = requests.get(f"{Config.URL_CLASS_CONTROL}/public/class/members", params=request.args)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Class Control Service unavailable", "details": str(e)}), 503

@syukra_teacher_bp.route('/teacher/assessment/class/', methods=['GET'])
@jwt_required()
@check_device_token
@check_permission('class_student_tab_teacher')
def get_assessment_by_class_id():
    try:
        response = requests.get(f"{Config.URL}/teacher/assessment/class", params=request.args)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Class Service unavailable", "details": str(e)}), 503

@syukra_teacher_bp.route('/teacher/assessment/', methods=['GET'])
@jwt_required()
@check_device_token
@check_permission('class_student_tab_teacher')
def get_assessment_by_id():
    try:
        response = requests.get(f"{Config.URL}/teacher/assessment", params=request.args)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Class Service unavailable", "details": str(e)}), 503
      
############################# CLASS DETAIL ########################
@syukra_teacher_bp.route('/kelas/weekly-section/class/', methods=['GET'])
@jwt_required()
@check_device_token
@check_permission('class_detail')
def get_class_detail_all_week():
    try:
        response = requests.get(f"{Config.URL_CLASS_CONTROL}/kelas/weekly-section/class", params=request.args)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Class Control Service unavailable", "details": str(e)}), 503
    
@syukra_teacher_bp.route('/kelas', methods=['GET'])
@jwt_required()
@check_device_token
@check_permission('class_detail')
def get_class_detail_by_id():
    try:
        response = requests.get(f"{Config.URL_CLASS_CONTROL}/kelas", params=request.args)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Class Control Service unavailable", "details": str(e)}), 503

@syukra_teacher_bp.route('/teacher/item-pembelajaran/', methods=['DELETE'])
@jwt_required()
@check_device_token
@check_permission('class_detail')
def delete_item_pembelajaran_by_uuid():
    try:
        response = requests.delete(f"{Config.URL_CONTENT}/item-pembelajaran", params=request.args)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Class Service unavailable", "details": str(e)}), 503
    
from flask import Response
@syukra_teacher_bp.route('/teacher/item-pembelajaran/', methods=['GET'])
@jwt_required()
@check_device_token
@check_permission('class_detail')
def get_item_pembelajaran_by_uuid():
    try:
        response = requests.get(f"{Config.URL_CONTENT}/item-pembelajaran", params=request.args, stream=True)
        
        return Response(
            response.iter_content(chunk_size=1024),
            content_type=response.headers.get('Content-Type'),
            status=response.status_code,
            headers=dict(response.headers)
        )
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Class Service unavailable", "details": str(e)}), 503
    
@syukra_teacher_bp.route('/teacher/kelas/weekly-section', methods=['POST'])
@jwt_required()
@check_device_token
@check_permission('class_detail')
def create_weekly_section():
    data = request.form.to_dict()
    file = request.files.get('file')

    if not data:
        return jsonify({"error": "Invalid input"}), 400

    # Konversi week_number ke integer jika ada
    if 'week_number' in data:
        try:
            data['week_number'] = int(data['week_number'])
        except ValueError:
            return jsonify({"error": "week_number must be an integer"}), 400
    try:
        files = {'file': (file.filename, file.stream, file.mimetype)} if file else None
        response = requests.post(
            f"{Config.URL_CLASS_CONTROL}/teacher/kelas/weekly-section",
            data=data,
            files=files
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Class Control Service unavailable",
            "details": str(e)
        }), 503
        
@syukra_teacher_bp.route('/teacher/kelas/weekly-section', methods=['PUT'])
@jwt_required()
@check_device_token
@check_permission('class_detail')
def update_weekly_section_teacher():
    data = request.form.to_dict()
    file = request.files.get('file')

    if not data:
        return jsonify({"error": "Invalid input"}), 400

    files = {'file': (file.filename, file.stream, file.mimetype)} if file else None

    try:
        response = requests.put(
            f"{Config.URL_CLASS_CONTROL}/teacher/kelas/weekly-section",
            data=data,
            files=files,
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Class Control Service unavailable",
            "details": str(e)
        }), 503

@syukra_teacher_bp.route('/teacher/kelas/assignment', methods=['PUT'])
@jwt_required()
@check_device_token
@check_permission('class_detail')
def update_assignment_teacher():
    data = request.form.to_dict()
    file = request.files.get('file')

    if not data:
        return jsonify({"error": "Invalid input"}), 400
    
    files = {'file': (file.filename, file.stream, file.mimetype)} if file else None

    try:
        response = requests.put(
            f"{Config.URL_CLASS_CONTROL}/teacher/kelas/assignment",
            data=data,
            files=files,
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Class Control Service unavailable",
            "details": str(e)
        }), 503

from werkzeug.utils import secure_filename

@syukra_teacher_bp.route('/teacher/kelas/assignment', methods=['POST'])
@jwt_required()
@check_device_token
@check_permission('class_detail')
def create_assignment():
    data = request.form.to_dict()
    file = request.files.get('file')

    if not data:
        return jsonify({"error": "Invalid input"}), 400

    # Siapkan file untuk dikirim via requests
    files = None
    if file:
        files = {
            'file': (secure_filename(file.filename), file.stream, file.mimetype)
        }

    # Ambil Authorization token dari header
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Authorization header missing"}), 401

    try:
        response = requests.post(
            f"{Config.URL_CLASS_CONTROL}/teacher/kelas/assignment",
            data=data,
            files=files,
            headers={"Authorization": auth_header}
        )
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": "Class Control Service unavailable",
            "details": str(e)
        }), 503

@syukra_teacher_bp.route('/teacher/kelas/weekly-section', methods=['DELETE'])
@jwt_required()
@check_device_token
@check_permission('class_detail')
def delete_weekly_section():
    try:
        response = requests.delete(f"{Config.URL_CLASS_CONTROL}/teacher/kelas/weekly-section", params=request.args)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Class Control Service unavailable", "details": str(e)}), 503
    

@syukra_teacher_bp.route('/teacher/kelas/assignment', methods=['DELETE'])
@jwt_required()
@check_device_token
@check_permission('class_detail')
def delete_assignment_teacher():
    try:
        response = requests.delete(f"{Config.URL_CLASS_CONTROL}/teacher/kelas/assignment", params=request.args)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Class Control Service unavailable", "details": str(e)}), 503
    