from flask import Blueprint

financial_bp = Blueprint('finiancial_bp', __name__)

from root.admin import views