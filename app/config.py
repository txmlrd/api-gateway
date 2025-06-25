import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    # Microservice URLs
    USER_SERVICE_URL = os.environ.get('USER_SERVICE_URL')
    AUTH_SERVICE_URL = os.environ.get('AUTH_SERVICE_URL')
    ROLE_SERVICE_URL = os.environ.get('ROLE_SERVICE_URL')
    
    # SYUKRA Service URLs
    URL_CLASS_CONTROL = os.environ.get('URL_CLASS_CONTROL')
    URL_CONTENT = os.environ.get('URL_CONTENT')
    URL = os.environ.get('URL')

    # Redis
    REDIS_URL = os.environ.get('REDIS_URL')

    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES'))  
    JWT_REFRESH_TOKEN_EXPIRES = int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRES'))  

    # JWT Header settings
    JWT_TOKEN_LOCATION = ['headers'] 
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
