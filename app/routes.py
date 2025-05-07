from flask import Blueprint, jsonify, request
import requests
api_gateway_bp = Blueprint('api_gateway', __name__)
from config import Config

@api_gateway_bp.route('/login', methods=['POST'])
def login():
    try:
        response = requests.post(
            f"{Config.USER_SERVICE_URL}/login",
            data=request.form  
        )
        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Auth service unreachable", "details": str(e)}), 503

@api_gateway_bp.route('/profile', methods=['GET'])
def profile():
    token = request.headers.get('Authorization').split(' ')[1]
    response = requests.get(f"{Config.USER_SERVICE_URL}/profile", headers={"Authorization": f"Bearer {token}"})
    if response.status_code == 200:
        return jsonify(response.json()), 200
    return jsonify({"error": "Failed to fetch profile"}), 400
