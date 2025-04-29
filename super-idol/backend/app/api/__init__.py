"""API 初始化模塊"""
from flask import Blueprint

bp = Blueprint('api', __name__)

from . import v1 