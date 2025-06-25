import redis
from flask_jwt_extended import decode_token
from app.config import Config

# Setup Redis connection
redis_client = redis.StrictRedis.from_url(Config.REDIS_URL)

def blacklist_token(jwt_token):
    if not jwt_token or jwt_token.count('.') != 2:
        raise ValueError("Invalid JWT token format")

    try:
        decoded_token = decode_token(jwt_token)
        jti = decoded_token.get('jti')
        if jti:
            redis_client.setex(f"blacklist_{jti}", 3600, 'blacklisted')  
    except Exception as e:
        raise ValueError(f"Failed to decode token: {str(e)}")

def is_token_blacklisted_by_jti(jti):
    return redis_client.exists(f"blacklist_{jti}") == 1
