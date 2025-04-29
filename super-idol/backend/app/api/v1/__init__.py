"""API v1 初始化模塊"""
from flask import Blueprint

bp = Blueprint('v1', __name__)

from . import auth, users, meals, food_items 