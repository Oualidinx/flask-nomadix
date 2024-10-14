from flask import url_for, redirect, render_template, flash, session
from root.admin import admin_bp
from flask_login import current_user, login_required
from root.admin.forms import RegistrationForm
import os, json
from root.models import User
from werkzeug.security import generate_password_hash

from root import database

from root.auth.views import send_reset_email

@admin_bp.get('/register')
@admin_bp.post('/register')
@login_required
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User()
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data

        user.role = "student"
        user.email = form.username.data
        user.password_hash = generate_password_hash(form.password.data, "scrypt")
        database.session.add(user)
        database.session.commit()
        flash(
            'Votre inscription a terminé avec succès. Un message a été transmis à votre adresse afin de confimer votre adresse',
            "success")
        #send_reset_email(user, "auth_bp.verify_email", subject='Email verification')
        session['new_reg'] = 1
        return redirect(url_for('auth_bp.login'))
    return render_template('admin/registration.html', form=form)