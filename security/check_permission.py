from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt
import logging

logging.basicConfig(level=logging.DEBUG)

def check_permission(permission_name):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            jwt_data = get_jwt()
            logging.debug(f"Claims: {jwt_data}")
            permissions = jwt_data.get("permissions", [])

            if permission_name not in permissions:
                return jsonify({"error": "Access denied"}), 403

            return f(*args, **kwargs)
        return wrapper
    return decorator
