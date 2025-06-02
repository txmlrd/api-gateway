from flask import Flask
from app.routes.adhi.auth import auth_bp
from app.routes.adhi.user import user_bp
from app.routes.admin import admin_bp
from app.routes.syukra.admin.admin import syukra_admin_bp
from app.routes.syukra.teacher.teacher import syukra_teacher_bp
from app.routes.syukra.student.student import syukra_student_bp
from app.routes.syukra.teacher_student import syukra_teacher_student_bp
from app.routes.adhi.role import role_permission_bp
from app.routes.adhi.storage import storage_bp
from extensions import jwt
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('config.Config')
    
    jwt.init_app(app)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(role_permission_bp)
    app.register_blueprint(syukra_admin_bp)
    app.register_blueprint(syukra_teacher_bp)
    app.register_blueprint(syukra_student_bp)
    app.register_blueprint(syukra_teacher_student_bp)
    app.register_blueprint(storage_bp)
    
    @app.route('/')
    def index():
        return 'User Service Running!'

    return app
