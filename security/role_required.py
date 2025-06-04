from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import get_jwt

def role_required(allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            identity = get_jwt()
            user_role = identity.get('role_name', None)
            if not user_role or user_role not in allowed_roles:
                return jsonify({"msg": "Access denied"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
