import redis
from config import Config
from security.redis_handler import is_token_blacklisted_by_jti
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, decode_token

redis_client = redis.StrictRedis.from_url(Config.REDIS_URL)
jwt = JWTManager()
create_access_token = create_access_token
jwt_required = jwt_required
get_jwt_identity = get_jwt_identity
decode_token = decode_token

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload.get("jti")
    return is_token_blacklisted_by_jti(jti)