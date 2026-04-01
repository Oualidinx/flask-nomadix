from flask import Blueprint

comm_bp = Blueprint('comm_bp', __name__,
                    template_folder='templates',
                    static_folder='static',
                    url_prefix="/commercial")

from root.admin import views