from flask import Flask

from config import configs
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager
from flask_mail import Mail
from flask_apscheduler import APScheduler
app = Flask(__name__)
database = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
scheduler = APScheduler()
def create_app(config_name):
    app.config.from_object(configs[config_name])


    from root.admin import admin_bp
    app.register_blueprint(admin_bp)

    from root.gestionnaire import emp_bp
    app.register_blueprint(emp_bp)

    from root.commercial import comm_bp
    app.register_blueprint(comm_bp)

    from root.financier import financial_bp
    app.register_blueprint(financial_bp)

    from root.auth import auth_bp
    app.register_blueprint(auth_bp)

    mail.init_app(app)
    database.init_app(app)
    login_manager.login_view="auth_bp.login"
    login_manager.login_message="Vieullez connecter pour utiliser ce service"
    login_manager.login_message_category="info"
    login_manager.init_app(app)
    # The task scheduler
    scheduler.init_app(app)
    scheduler.start()

    return app
