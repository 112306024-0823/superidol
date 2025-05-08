"""
Initialization file for the Flask application.
"""

from flask import Flask
from flask_cors import CORS
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS
    CORS(app)
    
    # Register blueprints
    from app.api import auth_bp, food_bp, exercise_bp, report_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(food_bp, url_prefix='/api/food')
    app.register_blueprint(exercise_bp, url_prefix='/api/exercise')
    app.register_blueprint(report_bp, url_prefix='/api/report')
    
    return app 