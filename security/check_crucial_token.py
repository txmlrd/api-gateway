from functools import wraps
from flask import request, jsonify
from app.extensions import redis_client
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

def check_crucial_token():
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            key = f"crucial_token:{user_id}"
            if not redis_client.get(key):
                  return jsonify({
                    "error": "CRUCIAL_FEATURE_AUTH_REQUIRED",
                    "message": "Crucial verification required",
                }), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator
