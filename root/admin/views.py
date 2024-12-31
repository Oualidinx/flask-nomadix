import datetime
import secrets

from flask import url_for, redirect, render_template, jsonify, session, abort, request, flash
from flask_login import current_user
from wtforms.validators import ValidationError

from forms import Subscription, PersonForm
from root.admin import admin_bp
from flask_login import login_required
from root.admin.forms import RegistrationForm, HotelForm, BusForm,GuideForm, VoyagesForm
from flask_weasyprint import HTML, render_pdf
from root.models import *
from werkzeug.security import generate_password_hash

from root import database


@admin_bp.get('/')
@login_required
def index():
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

    return render_template('admin/users.html', liste=liste)


@admin_bp.get('/buses')
@admin_bp.post('/buses')
@login_required
def buses():
    session['endpoint'] = 'buses'
    _buses = Bus.query.filter_by(is_deleted = False).all()
    # print(_users)
    liste = list()
    if _buses:
        for b in _buses:
            liste.append(b.repr(
                columns=['id',
                         'driver_full_name',
                         'capacity',
                         'company',
                         'contacts']))
    return render_template('admin/buses.html', liste=liste)


@admin_bp.get('/guides')
@admin_bp.post('/guides')
@login_required
def guides():
    session['endpoint'] = 'guides'
    _guide = Guide.query.filter_by(is_deleted = False).all()
    # print(_users)
    liste = list()
    if _guide:
        for b in _guide:
            liste.append(b.repr(
                columns=['id',
                         'name',
                         'sex',
                         '#voyages']))
    return render_template('admin/guides.html', liste=liste)


@admin_bp.get('/hotels')
# @admin_bp.post('/hotels')
@login_required
def hotels():
    session['endpoint'] = 'hotels'
    _hotels = Hotel.query.filter_by(is_deleted = False).all()
    # print(_users)
    liste = list()
    if _hotels:
        for b in _hotels:
            liste.append(b.repr(
                columns=['id',
                         'name',
                         'star_rating',"#voyages"]))
    return render_template('admin/hotels.html', liste=liste)



@admin_bp.get('/voyages')
@admin_bp.get('/voyages')
# @admin_bp.post('/voyages')
@login_required
def voyages():
    session['endpoint'] = 'voyages'
    _voyages = Voyage.query.filter_by(is_deleted = False).all()
    liste = list()
    if _voyages:
        for b in _voyages:
            liste.append(b.repr(
                columns=['id',"destination","created_by","date_depart","date_end"]
            ))
    return render_template('admin/voyages.html', liste=liste)



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


@admin_bp.post('/users/get')
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



@admin_bp.post('/buses/get')
@login_required
def get_bus():
    session['endpoint'] = 'buses'

    data = request.json
    b = Bus.query.get(int(data['bus_id']))
    if not b:
        abort(404)
    contacts_str = ""
    i=1
    for c in b.contacts:
        contacts_str += (f"<span>        </span>{i} - <span class='fw-bold mb-3'>Nom: {c.name}</span> <br> "
                         f"<span>               </span><span class='fw-bold mb-3'>Numéro de téléphone: {c.phone}</span> <br>\n")
        i+=1
    return jsonify(message=f"<h4 class='h4 fw-bold'>{b.company}</h4> \
                        <span class='fw-bold mb-3'>Conducteur: </span>{b.driver_full_name} <br> \
                        <span class='fw-bold mb-3'>Nombre de places: </span>{b.capacity} <br> \
                        <span class='fw-bold mb-3'>Contacts: </span> <br>"+contacts_str
                           ), 200


@admin_bp.post('/guides/get')
@login_required
def get_guide():
    session['endpoint'] = 'guides'

    data = request.json
    b = Guide.query.get(int(data['guide_id']))
    if not b:
        abort(404)
    contacts_str = ""
    i=1
    for c in b.contacts:
        contacts_str += (f"<span>        </span>{i} - <span class='fw-bold mb-3'>Nom:</span> {c.name} <br> "
                         f"<span>               </span><span class='fw-bold mb-3'>Numéro de téléphone: </span> {c.phone} <br>\n")
        i+=1
    return jsonify(message=f"<h4 class='h4 fw-bold'>{b.name}</h4>"
                           f"<span class='fw-bold mb-3'>Nombre de voyages: </span>{b.repr(['#voyages'])['#voyages']} <br>"
                           f"<span class='fw-bold mb-3'>Sexe: </span>{b.sex} <br> "
                           f"<span class='fw-bold mb-3'>Contacts: </span> <br>" + contacts_str), 200


@admin_bp.post('/hotels/get')
@login_required
def get_hotel():
    session['endpoint'] = 'hotels'

    data = request.json
    b = Hotel.query.get(int(data['hotel_id']))
    if not b:
        abort(404)
    contacts_str = ""
    i=1
    for c in b.contacts:
        contacts_str += (f"<span>        </span>{i}) <span class='fw-bold mb-3'>Nom:</span> {c.name}  "
                         f"<br><span style=\"color:white;\">....</span><span class='fw-bold mb-3'>Numéro de téléphone: </span> {c.phone} <br>\n")
        i+=1
    return jsonify(message=f"<h4 class='h4 fw-bold'>Hôtel {b.name}</h4>"
                           f"<span class='fw-bold mb-3'>Classement par étoiles: </span>{b.repr(['star_rating'])['star_rating']} étoiles(s)<br>"
                           f"<span class='fw-bold mb-3'>Contacts: </span> <br>" + contacts_str), 200
@admin_bp.post('/voyages/get')
@login_required
def get_voyage():
    session['endpoint'] = 'voyages'
    data = request.json
    v = Voyage.query.get(int(data['voyage_id']))
    if not v:
        abort(404)
    include = Include.query.filter_by(fk_voyage_id=v.id).first()
    if not include:
        return render_template("errors/page-404.html", blueprint="admin_bp")
    bus = None
    if include.fk_bus_id:
        bus = Bus.query.get(include.fk_bus_id)
    else:
        bus = "/"
    guide = None
    if include.fk_guide_id:
        guide = Guide.query.get(include.fk_bus_id)
    else:
        guide = "/"

    _dict = v.repr()
    return jsonify(
        message=f"<h3 class='h3 fw-bold'>Excursion vers {_dict['destination']}</h3>"
                f"<br><span class='fw-bold mb-3'> Date de départ: </span>{_dict['date_depart']}<br>"
                f"<br><span class='fw-bold mb-3'> Date de retour: </span>{_dict['date_end']}<br>"
                f"<br><span class='fw-bold mb-3'> Date de clôture des inscriptions: </span>{_dict['subscription_due_date']}<br>"
                f"<br><span class='fw-bold mb-3'> Bus: </span>{_dict['is_bus_included']}<br>"
                f"<br><span class='fw-bold mb-3'> Companie de bus: </span>{_dict['bus_company']}<br>"
                f"<br><span class='fw-bold mb-3'> Guide: </span>{_dict['is_guide_included']}<br>"
                f"<br><span class='fw-bold mb-3'> Nom du guide: </span>{_dict['guide_full_name']}<br>"
                f"<br><span class='fw-bold mb-3'> Hôtel: </span>{_dict['is_hotel_included']}<br>"
                f"<br><span class='fw-bold mb-3'> Nom de l'hôtel: </span>{_dict['hotel_name']}<br>"
                f"<br><span class='fw-bold mb-3'> Avion: </span>{_dict['is_plane_included']}<br>"
                f"<br><span class='fw-bold mb-3'> Visa: </span>{_dict['is_visa_included']}<br>"
    ), 200



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


@admin_bp.get('/buses/<int:bus_id>/delete')
@login_required
def delete_bus(bus_id):
    bus = Bus.query.get(bus_id)
    if not bus:
        return render_template("errors/404.html", blueprint="admin_bp")

    if bus.is_deleted:
        flash('Erreur', 'danger')
        return redirect(url_for("admin_bp.buses"))
    bus.is_deleted = True
    database.session.add(bus)
    database.session.commit()
    if len(bus.voyages) == 0:
        for c in bus.contacts:
            database.session.delete(c)
            database.session.commit()
        database.session.delete(bus)
        database.session.commit()
    flash('Opération se termine avec succès', "success")
    return redirect(url_for("admin_bp.buses"))


@admin_bp.get('/guides/<int:guide_id>/delete')
@login_required
def delete_guide(guide_id):
    guide = Guide.query.get(guide_id)
    if not guide:
        return render_template("errors/404.html", blueprint="admin_bp")

    if guide.is_deleted:
        flash('Erreur', 'danger')
        return redirect(url_for("admin_bp.guides"))
    guide.is_deleted = True
    database.session.add(guide)
    database.session.commit()
    if len(guide.voyages) == 0:
        for c in guide.contacts:
            database.session.delete(c)
            database.session.commit()
        database.session.delete(guide)
        database.session.commit()
    flash('Opération se termine avec succès', "success")
    return redirect(url_for("admin_bp.guides"))


@admin_bp.get('/hotels/<int:hotel_id>/delete')
@login_required
def delete_hotel(hotel_id):
    hotel = Hotel.query.get(hotel_id)
    if not hotel:
        return render_template("errors/404.html", blueprint="admin_bp")

    if hotel.is_deleted:
        flash('Erreur', 'danger')
        return redirect(url_for("admin_bp.hotels"))
    hotel.is_deleted = True
    database.session.add(hotel)
    database.session.commit()
    if len(hotel.voyages) == 0:
        for c in hotel.contacts:
            database.session.delete(c)
            database.session.commit()
        database.session.delete(hotel)
        database.session.commit()
    flash('Opération se termine avec succès', "success")
    return redirect(url_for("admin_bp.hotels"))


@admin_bp.get("/voyages/<int:voyage_id>/delete")
@login_required
def delete_voyage(voyage_id):
    voyage = Voyage.query.get(voyage_id)
    if not voyage:
        return render_template("errors/page-404.html", blueprint="admin_bp")
    include=Include.query.filter_by(fk_voyage_id=voyage_id).first()
    if not include:
        return render_template("errors/404.html", blueprint="admin_bp")
    database.session.delete(include)
    database.session.commit()
    database.session.delete(voyage)
    database.session.commit()
    flash('Suppression avec succès', 'success')
    return redirect(url_for("admin_bp.voyages"))


@admin_bp.get('/hotels/new')
@admin_bp.post('hotels/new')
@login_required
def add_hotel():
    form = HotelForm()
    if form.validate_on_submit():
        hotel = Hotel()
        hotel.name = form.name.data
        hotel.star_rating = int(form.star_rating.data)
        database.session.add(hotel)
        database.session.commit()

        contact = Contact()
        contact.name = f"Numéro de téléphone de l'hotel: {hotel.name}"
        contact.phone = form.phone_number.data
        contact.fk_hotel_id = hotel.id
        database.session.add(contact)
        database.session.commit()
        flash('Opération terminé avec succès','success')
        return redirect(url_for("admin_bp.hotels"))
    return render_template('admin/new_hotel.html',form=form)


@admin_bp.get('/buses/new')
@admin_bp.post('buses/new')
@login_required
def add_bus():
    form = BusForm()
    if form.validate_on_submit():
        bus = Bus()
        bus.company = form.company.data
        bus.driver_full_name = form.driver_full_name.data
        bus.capacity= form.capacity.data
        bus.state = form.state.data if form.state.data else None
        database.session.add(bus)
        database.session.commit()

        contact = Contact()
        contact.name = f"Numéro de téléphone du conducteur : {bus.driver_full_name} Bus de: {bus.company}"
        contact.phone = form.drivers_phone_number.data
        contact.fk_bus_id = bus.id
        database.session.add(contact)
        database.session.commit()
        flash('Opération terminée avec succès','success')
        return redirect(url_for("admin_bp.buses"))
    else:
        print(form.errors)
    return render_template('admin/new_bus.html', form = form)

import os
@admin_bp.get('/guides/new')
@admin_bp.post('guides/new')
@login_required
def add_guide():
    form = GuideForm()
    current_dir = os.getcwd()
    # print(current_dir)
    os.chdir(current_dir + "/root/static/uploads")

    file = open("algeria_postcodes.json", "r")

    data = json.load(file)
    states = [(x['wilaya_name'], x['wilaya_code'] + '-' + x['wilaya_name']) for x in data]
    states = list(dict.fromkeys(states))
    os.chdir(current_dir)
    form.state.choices = states
    if form.validate_on_submit():
        print(form.data)
        guide = Guide()
        guide.name = form.full_name.data
        guide.sex = form.sex.data

        guide.state = form.state.data if form.state.data else None
        database.session.add(guide)
        database.session.commit()
        contact = Contact()
        contact.name = f"Numéro de téléphone du guide : {guide.name} de: {guide.state}"
        contact.phone = form.guide_phone_number.data
        contact.fk_guide_id = guide.id
        database.session.add(contact)
        database.session.commit()
        flash('Opération terminée avec succès','success')
        return redirect(url_for("admin_bp.guides"))
    return render_template('admin/new_guide.html', form = form)


@admin_bp.get('/voyages/new')
@admin_bp.post('/voyages/new')
@login_required
def add_voyage():
    form = VoyagesForm()
    if form.validate_on_submit():
        voyage = Voyage()
        voyage.destination = form.destination.data
        voyage.date_depart = form.date_depart.data
        voyage.date_end=form.date_end.data
        voyage.subscription_due_date = form.subscription_due_date.data+datetime.timedelta(hours=23, minutes=59, seconds=59)
        # voyage.bus_company = form.bus_company.data if form.is_bus_included.data else None
        voyage.is_bus_included = True if form.is_bus_included.data else False
        voyage.bus_fees = int(form.bus_fees.data) if form.is_bus_included.data else None
        voyage.is_hotel_included = True if form.is_hotel_included.data else False
        voyage.hotel_fees = int(form.hotel_fees.data) if form.hotel_fees.data else None
        voyage.is_plane_included = True if form.is_plane_included.data else False
        voyage.plane_fees= int(form.avion_fees.data) if form.avion_fees.data else None
        voyage.visa_fees = int(form.visa_fees.data) if form.visa_fees.data else None
        voyage.is_guide_included = True if form.is_guide_included.data else False
        voyage.guide_fees = int(form.guide_fees.data) if form.guide_fees.data else None
        voyage.created_by = current_user.id
        database.session.add(voyage)
        database.session.commit()

        include = Include()
        include.fk_voyage_id=voyage.id
        include.fk_hotel_id = form.hotel.data.id if (form.hotel.data and
                                                       Hotel.query.get(form.hotel.data.id) and
                                                       voyage.is_hotel_included==True) else None
        include.fk_bus_id = form.bus_company.data.id if (form.bus_company.data
                                                           and Bus.query.get(form.bus_company.data.id)
                                                           and voyage.is_bus_included==True) else None
        include.fk_guide_id = form.guides.data.id if (form.guides.data
                                                        and  Guide.query.get(form.guides.data.id)
                                                        and voyage.is_guide_included == True) else None
        database.session.add(include)
        database.session.commit()
        flash('Operation terminée avec succès','success')
        return redirect(url_for("admin_bp.voyages"))
    return render_template("admin/new_voyages.html", form=form)


@admin_bp.get('/voyages/<int:voyage_id>/subscription')
@admin_bp.post('/voyages/<int:voyage_id>/subscription')
@login_required
def subscription(voyage_id):
    voyage = Voyage.query.filter_by(is_deleted=False).filter_by(id=voyage_id).first()
    if not voyage:
        return render_template('errors/404.html', blueprint="admin_bp")

    if voyage.subscription_due_date > datetime.now():
        flash("Inscription fermé, vous ne pouvez pas procèder d'autres", "warnings")
        return redirect(url_for("admin_bp.voyages"))
    form=Subscription()
    if form.validate_on_submit():
        agency = Agency()
        agency.label = form.label.data
        agency.reserved_places = form.reserved_places.data
        entities = list()
        if enumerate(form.persons):
            _ = Person()
            for _index, entry in enumerate(form.persons):
                if entry.delete_entry.data:
                    del form.persons.entries[_index]
                    return render_template("admin/subscription.html",
                                           form=form, nested=PersonForm())
                _.first_name = entry.first_name.data if entry.first_name.data else None
                _.last_name = entry.last_name.data if entry.last_name.data else None

                entities.append(_)
        if form.add.data:
            form.persons.append_entry({
                'first_name': "",
                'last_name': "",
                "sexe":""
            })
            return render_template('admin/subscription.html', form=form, nested=PersonForm())
        database.session.add(agency)
        database.session.commit()
        v_for_a = VoyageForAgency()
        v_for_a.fk_voyage_id = voyage.id
        v_for_a.fk_agency_id=agency.id
        database.session.add(v_for_a)
        database.session.commit()

        for e in entities:
            e.fk_agency_id = agency.id
            db.session.add(e)
            db.session.commit()
        flash('Inscription crée avec succès', 'success')
        return redirect(url_for("admin_bp.voyages"))
    return render_template('admin/subscription.html', form=form, nested=PersonForm())
