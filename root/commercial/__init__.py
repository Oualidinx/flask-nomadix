from flask import Blueprint

comm_bp = Blueprint('comm_bp', __name__)

from root.admin import views