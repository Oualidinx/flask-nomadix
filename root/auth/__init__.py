from flask import Blueprint, url_for

auth_bp = Blueprint('auth_bp',__name__, url_prefix="/auth")

from root.auth import views