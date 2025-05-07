from flask import Flask
from app.routes.auth import auth_bp
from extensions import jwt

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    jwt.init_app(app)

    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
