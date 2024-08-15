from flask import Flask
from .routes import routes_bp

def create_app():
    app = Flask(__name__)

    app.config.from_object('app.config.Config')

    # Register blueprints
    app.register_blueprint(routes_bp)

    return app