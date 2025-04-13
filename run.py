from root import create_app, database as db
from flask import redirect, url_for
from root.models import *
import os

from dotenv import load_dotenv

load_dotenv('.env')
application = create_app(os.environ.get('FLASK_ENV'))


@application.route('/')
def index():
    return redirect(url_for('auth_bp.login'))


# if __name__ == "__main__":
#     application.run(debug=False)