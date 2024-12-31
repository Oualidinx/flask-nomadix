from flask import url_for, redirect, request, render_template, flash, session
from root.auth import auth_bp
from root.models import User
from flask_login import login_required, login_user, logout_user
from root.auth.forms import LoginForm
from werkzeug.security import check_password_hash
from root import mail, login_manager
import os


def send_reset_email(user, url, subject):
    user_name = os.environ.get('MAIL_USERNAME')
    if user.role!="master" and user.is_deleted==0:
        # msg.body = render_template('verify_email.html', url = url_for(url, token=user.get_token(), _external=True))
        mail.send(subject=subject,
                              sender=user_name,  # from domain
                              receivers=[user.email],
                          html=f'''<head>
                    <meta charset="UTF-8">
                    <meta http-equiv="X-UA-Compatible" content="IE=edge">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <link href="{url_for('static', filename='css/tailwind.min.css')}" rel="stylesheet">
                </head>
                <body>
                    <div class="flex items-center justify-center min-h-screen p-5 bg-blue-100 min-w-screen">
                        <div class="max-w-xl p-8 text-center text-gray-800 bg-white shadow-xl lg:max-w-3xl rounded-3xl lg:p-12">
                            <p>Pour compléter Le service demandé, veuillez d'abord confirmer votre email afin d'être sûre de vous !</p>
                            <p style="font-weight: bold;">Important: Vous avez que 5 minutes pour terminer ce processus</p>
                            <div class="mt-4">
                                <a role="button" href="{url_for(url, token=user.get_token(300), _external=True)}" class="px-2 py-2 text-blue-200 bg-blue-600 rounded">Cliquez Ici pour confirmer votre adresse électronique</a>
                            </div>
                        </div>
                    </div>
                </body>
                '''
              )


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    """if request.method=="GET":
        if 'new_reg' in session:
            del session ['new_reg']"""
    if form.validate_on_submit():
        user = User.query.filter_by(is_deleted=0) \
                            .filter_by(username=form.username.data) \
                            .first()
        if user:
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user, remember=False)
                nex_page = request.args.get('next')
                if nex_page:
                    return redirect(nex_page)
                if user.role == "master":
                    return redirect(url_for('admin_bp.index'))
                if user.role == "financier":
                    return redirect(url_for('financial_bp.index'))
                if user.role == "gestionnaire":
                    return redirect(url_for('emp_bp.index'))
                # if user.role == "commercial":
                return redirect(url_for('comm_bp.index'))
            else:
                flash('Veuillez vérifier les  informations', 'danger')
                return render_template('auth/login.html', form=form)

        else:
            flash('veuillez verifier les informations', 'danger')
            # return redirect(url_for('auth_bp.login'))
    return render_template('auth/login.html', form=form)


@auth_bp.get('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('auth_bp.login'))