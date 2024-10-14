from flask import Blueprint

admin_bp = Blueprint('admin_bp', __name__)

from root.admin import views