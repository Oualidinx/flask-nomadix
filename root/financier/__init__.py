from flask import Blueprint

financial_bp = Blueprint('financial_bp', __name__, url_prefix="/financial")

from . import views