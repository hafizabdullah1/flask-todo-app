from flask import Flask
from config import Config
from app.extensions import db, login_manager

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register Blueprints
    from app.routes.todos import todos_bp
    from app.routes.auth import auth_bp
    app.register_blueprint(todos_bp)
    app.register_blueprint(auth_bp)

    # Create tables if they do not exist
    with app.app_context():
        db.create_all()

    return app
