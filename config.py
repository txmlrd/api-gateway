import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    # Microservice URLs
    USER_SERVICE_URL = os.environ.get('USER_SERVICE_URL')

    # Redis
    REDIS_URL = os.environ.get('REDIS_URL')

    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 3600))  # 1 hour
    JWT_REFRESH_TOKEN_EXPIRES = int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRES', 86400))  # 24 hours

    # JWT Header settings
    JWT_TOKEN_LOCATION = ['headers']  # Harus list, bukan string
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
