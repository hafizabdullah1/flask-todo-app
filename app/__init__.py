from flask import Flask
from config import Config
from app.extensions import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with this app
    db.init_app(app)

    # Register Blueprints
    from app.routes.todos import todos_bp
    app.register_blueprint(todos_bp)

    # Create tables if they don't exist
    with app.app_context():
        db.create_all()

    return app
    