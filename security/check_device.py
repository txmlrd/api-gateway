from functools import wraps
from flask_jwt_extended import get_jwt
from flask import jsonify
from app.extensions import redis_client, get_jwt_identity

def check_device_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()
        current_jti = get_jwt()['jti']
        stored_jti = redis_client.get(f"user_active_token:{user_id}")

        if stored_jti and stored_jti.decode() != current_jti:
            return jsonify({"msg": "Another device is logged in"}), 403

        return f(*args, **kwargs)
    return decorated_function
