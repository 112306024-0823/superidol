"""
API blueprints initialization.
"""

from app.api.auth import auth_bp
from app.api.food import food_bp
from app.api.exercise import exercise_bp
from app.api.report import report_bp





__all__ = ['auth_bp', 'food_bp', 'exercise_bp', 'report_bp'] 

