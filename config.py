import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    USER_SERVICE_URL = os.environ.get('USER_SERVICE_URL')
    # Sesuaikan URL sesuai dengan service yang kamu punya
