from flask import Blueprint, session, jsonify, request
from extensions import jwt_required, get_jwt_identity
from security.check_device import check_device_token
import requests
from config import Config
from security.check_permission import check_permission
from security.check_crucial_token import check_crucial_token
from werkzeug.utils import secure_filename
from flask import Response

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
@check_device_token
@check_permission('manage_profile')
def profile():
    token = request.headers.get('Authorization').split(' ')[1]
    response = requests.get(f"{Config.USER_SERVICE_URL}/profile", headers={"Authorization": f"Bearer {token}"})
    if response.status_code == 200:
        return jsonify(response.json()), 200
    return jsonify({"error": "Failed to fetch profile"}), 400

@user_bp.route('/register', methods=['POST'])
def register():
    try:
        # Ambil data dan file dari request asli
        form_data = request.form
        files = [('face_reference', file) for file in request.files.getlist('face_reference')]

        # Kirim form dan file ke User Service
        response = requests.post(
            f"{Config.USER_SERVICE_URL}/register",
            data=form_data,
            files=files
        )
        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "User Service unavailable", "details": response.json()}), 503

@user_bp.route('/verify-email/<token>', methods=["GET"])
def proxy_verify_email(token):
    try:
        response = requests.get(f"{Config.USER_SERVICE_URL}/verify-email/{token}")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException:
        return jsonify({"msg": "Failed to connect to Auth Service"}), 500


    
@user_bp.route('/update', methods=['POST'])
@jwt_required()
@check_device_token
@check_permission('manage_profile')
@check_crucial_token()
def update_profile():
    token = request.headers.get('Authorization').split(' ')[1]
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400
    try:
        response = requests.post(f"{Config.USER_SERVICE_URL}/update", headers={"Authorization": f"Bearer {token}"}, json=data, timeout=5)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "User Service unavailable", "details": str(e)}), 503
    
@user_bp.route('/update/face-reference', methods=['POST'])
@jwt_required()
@check_device_token
@check_permission('manage_profile')
def update_face_reference():
    token = request.headers.get('Authorization').split(' ')[1]
    files = [('images', file) for file in request.files.getlist('images')]
    try:
        response = requests.post(f"{Config.USER_SERVICE_URL}/update/face-reference", headers={"Authorization": f"Bearer {token}"}, files=files, timeout=5)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "User Service unavailable", "details": str(e)}), 503
    
@user_bp.route('/update/email', methods=['POST'])
@jwt_required()
@check_device_token
@check_permission('manage_profile')
@check_crucial_token()
def update_email():
    token = request.headers.get('Authorization').split(' ')[1]
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400
    try:
        response = requests.post(f"{Config.USER_SERVICE_URL}/update/email/request", headers={"Authorization": f"Bearer {token}"}, json=data)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "User Service unavailable", "details": str(e)}), 503

@user_bp.route('/update/email/confirm/<token>', methods=['GET'])
def confirm_email_update(token):
    try:
        response = requests.get(f"{Config.USER_SERVICE_URL}/update/email/confirm/{token}")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "User Service unavailable", "details": str(e)}), 503

@user_bp.route('/update/face-model-preference', methods=['POST'])
@jwt_required()
@check_device_token
@check_permission('manage_profile')
def update_face_model_preference():
    token = request.headers.get('Authorization').split(' ')[1]
    data = request.form
    try:
        response = requests.post(f"{Config.USER_SERVICE_URL}/update/face-model-preference", headers={"Authorization": f"Bearer {token}"}, data=data, timeout=5)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "User Service unavailable", "details": str(e)}), 503
    

@user_bp.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
@check_device_token
@check_permission('manage_profile')
@check_crucial_token()
def delete_profile(id):
    token = request.headers.get('Authorization').split(' ')[1]
    try:
        response = requests.delete(f"{Config.USER_SERVICE_URL}/delete/{id}", headers={"Authorization": f"Bearer {token}"}, timeout=5)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "User Service unavailable", "details": str(e)}), 503
    
@user_bp.route('/reset-password/request', methods=['POST'])
def reset_password_request():
    data = request.get_json()
    try:
        response = requests.post(f"{Config.USER_SERVICE_URL}/reset-password/request", json=data, timeout=5)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "User Service unavailable", "details": str(e)}), 503

@user_bp.route('/reset-password/confirm/<token>', methods=['GET','POST'])
def reset_password_proxy(token):
    auth_service_url = f"{Config.USER_SERVICE_URL}/reset-password/confirm/{token}"

    try:
        if request.method == 'GET':
            resp = requests.get(auth_service_url)
        else:  # POST
            resp = requests.post(auth_service_url, data=request.form)

        # Kirim response HTML dari auth service langsung ke user
        return Response(resp.content, status=resp.status_code, content_type=resp.headers.get('Content-Type'))

    except requests.exceptions.RequestException as e:
        return "Auth Service is unavailable", 503
    


@user_bp.route('/update/profile-picture', methods=['POST'])
@jwt_required()
@check_device_token
@check_permission('manage_profile')
def update_profile_picture():
    token = request.headers.get('Authorization').split(' ')[1]
    files = []

    for file in request.files.getlist('profile_picture'):
        filename = secure_filename(file.filename)
        if not filename.lower().endswith('.jpg'):
            return jsonify({"error": "Only .jpg files are allowed"}), 400
        files.append(('profile_picture', (filename, file.stream, file.mimetype)))

    try:
        response = requests.post(
            f"{Config.USER_SERVICE_URL}/update/profile-picture",
            headers={"Authorization": f"Bearer {token}"},
            files=files
        )
        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "User Service unavailable", "details": str(e)}), 503

    
