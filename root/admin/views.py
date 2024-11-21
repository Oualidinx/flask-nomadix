import secrets

from flask import url_for, redirect, render_template, jsonify, session, abort, request, flash
from root.admin import admin_bp
from flask_login import login_required
from root.admin.forms import RegistrationForm
from flask_weasyprint import HTML, render_pdf
from root.models import *
from werkzeug.security import generate_password_hash

from root import database


@admin_bp.get('/')
@login_required
def home():
    return render_template('layouts/admin_home.html')

@admin_bp.get('/users')
@admin_bp.post('/users')
@login_required
def users():
    session['endpoint'] = 'users'
    _users = User.query.filter_by(is_deleted = False).all()
    # print(_users)
    liste = list()
    if _users:
        for user in _users:
            liste.append(user.repr(columns=['id', 'full_name', 'username','role', 'phone_number']))
    print(liste)
    return render_template('admin/users.html', liste=liste)


@admin_bp.get('/buses')
@admin_bp.post('/buses')
@login_required
def users():
    session['endpoint'] = 'buses'
    _users = Bus.query.filter_by(is_deleted = False).all()
    # print(_users)
    liste = list()
    if _users:
        for user in _users:
            liste.append(user.repr(columns=['id', 'full_name', 'username','role', 'phone_number']))
    return render_template('admin/users.html', liste=liste)


@admin_bp.get('/users/register')
@admin_bp.post('/users/register')
@login_required
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
    return render_template('admin/add_user.html', form=form)


@admin_bp.get('/print')
@login_required
def print_credentials():
    html = render_template('admin/credentials.html',
                           username = session['username'],
                           password = session['password'])
    return render_pdf(HTML(string=html))


@admin_bp.post('/employees/get')
@login_required
def get_user():
    session['endpoint'] = 'users'

    data = request.json
    user = User.query.get(int(data['user_id']))
    if not user:
        abort(404)
    return jsonify(message=f"<h4 class='h4 fw-bold'>{user.first_name} {user.last_name}</h4> \
                        <span class='fw-bold mb-3'>Pseudonyme: </span>{user.username} <br> \
                        <span class='fw-bold mb-3'>Rôle: </span>{user.role} <br> \
                        <span class='fw-bold mb-3'>Numéro de téléphone: </span>{user.phone_number}"), 200


# @admin_bp.post('/users/<int:user_id>/update')
# # @login_required
# def edit_user(user_id):
#     user = User.query.filter_by(is_deleted = False).get(user_id)
#     if user is None:
#         abort(404)
#     return redirect(url_for("admin_bp.users"))


@admin_bp.get('/users/<int:user_id>/delete')
@login_required
def delete(user_id):
    user = User.query.get(user_id)
    if not user:
        return render_template("errors/404.html", blueprint="admin_bp")

    if user.is_deleted:
        flash('Erreur', 'danger')
        return redirect(url_for("admin_bp.users"))
    user.is_deleted = True
    database.session.add(user)
    database.session.commit()
    flash('Opération se termine avec succès', "success")
    return redirect(url_for("admin_bp.users"))