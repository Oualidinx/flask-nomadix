import secrets

from flask import url_for, redirect, render_template, flash, session
from root.admin import admin_bp
from flask_login import login_required
from root.admin.forms import RegistrationForm
from flask_weasyprint import HTML, render_pdf
from root.models import User
from werkzeug.security import generate_password_hash

from root import database

from root.auth.views import send_reset_email


@admin_bp.get('/')
@login_required
def home():
    return render_template('layouts/admin_home.html')

@admin_bp.get('/users')
@admin_bp.post('/users')
# @login_required
def users():
    session['endpoint'] = 'users'
    _users = User.query.filter_by(is_deleted = False).all()
    liste = list()
    if _users:
        for user in _users:
            liste.append(user.repr(columns=['id', 'full_name', 'username','role', 'phone_number']))
    return render_template('admin/users.html', liste=liste)
@admin_bp.get('/users/register')
@admin_bp.post('/users/register')
# @login_required
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User()
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data

        user.role = form.role.data
        session['username'] = secrets.token_urlsafe(8)
        user.username = session['username']
        session['password'] = secrets.token_urlsafe(6)
        user.password_hash = generate_password_hash(session['password'], "scrypt")
        database.session.add(user)
        database.session.commit()
        # send_reset_email(user, "auth_bp.verify_email", subject='Email verification)
        form = RegistrationForm()
        return redirect(url_for("admin_bp.print_credentials"))
    else:
        print(form.errors)
    return render_template('admin/add_user.html', form=form)


@admin_bp.get('/print')
# @login_required
def print_credentials():
    html = render_template('admin/credentials.html',
                           username = session['username'],
                           password = session['password'])
    return render_pdf(HTML(string=html))


"""
@auth_bp.get("/reset_password/<string:token>")
@auth_bp.post("/reset_password/<string:token>")
def reset_password(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash('Il y a une erreur', 'warning')
        return redirect(url_for('auth_bp.request_token'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password_hash = generate_password_hash(form.new_password.data, "SHA256")
        database.session.add(user)
        database.session.commit()
        flash('Votre mot de passe a été changé avec succès', 'success')
        return redirect(url_for('auth_bp.login'))
    return render_template("reset_password.html", form=form)"""