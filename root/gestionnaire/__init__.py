from flask import Blueprint

emp_bp = Blueprint('emp_bp', __name__, url_prefix='/gestionnaire')

from . import views