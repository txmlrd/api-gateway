from flask import Blueprint, jsonify, request
from extensions import jwt_required
from security.check_device import check_device_token
import requests
from config import Config

from flask import Response

storage_bp = Blueprint('storage_bp', __name__)

@storage_bp.route('/storage/user_profile_pictures/<filename>', methods=['GET'])
def proxy_profile_picture(filename):
    try:
        response = requests.get(
            f"{Config.USER_SERVICE_URL}/user_profile_pictures/{filename}",
            stream=True
        )
        if response.status_code == 200:
            return Response(
                response.iter_content(chunk_size=1024),
                content_type=response.headers.get('Content-Type')
            )
        else:
            return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "User Service unavailable", "details": str(e)}), 503