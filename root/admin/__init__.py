from flask import Blueprint

admin_bp = Blueprint('admin_bp', __name__, url_prefix="/admin")

from root.admin import views