from flask import Blueprint

emp_bp = Blueprint('emp_bp', __name__)

from root.gestionnaire import views