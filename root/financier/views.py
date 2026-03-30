import json

from flask import render_template, flash, redirect, url_for
from . import financial_bp
from flask_login import login_required

from root import database
from root.forms import HotelForm, GuideForm, BusForm, ConfigForm
from root.models import Hotel, Contact, Guide, Bus, Agency, Config
from flask import session

@financial_bp.route('/')
@financial_bp.route('/dashboard')
@login_required
def index():
    return render_template("financier/dashboard.html")


@financial_bp.get('/hotels')
@login_required
def hotels():
    session['endpoint'] = 'suppliers'
    _hotels = Hotel.query.filter_by(is_deleted=False).all()
    liste = list()
    if _hotels:
        for b in _hotels:
            liste.append(b.repr(
                columns=['id',
                         'name',
                         'star_rating',
                         "#voyages"]))
    return render_template("financier/hotels.html", liste = liste)


@financial_bp.get('/hotels/<int:hotel_id>')
@login_required
def hotel_detail(hotel_id):
    hotel = Hotel.query.get(hotel_id)
    if not hotel:
        return render_template('errors/404.html', blueprint="financial_bp"), 404
    return render_template("financier/hotel-view.html", hotel = hotel.repr())


@financial_bp.get('/buses')
@login_required
def buses():
    session['endpoint'] = 'suppliers'
    _buses = Bus.query.filter_by(is_deleted=False).all()
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
    return render_template("financier/buses.html", liste = liste)


@financial_bp.get('/guides')
@login_required
def guides():
    session['endpoint'] = 'suppliers'
    _guide = Guide.query.filter_by(is_deleted=False).all()
    # print(_users)
    liste = list()
    if _guide:
        for b in _guide:
            liste.append(b.repr(
                columns=['id',
                         'name',
                         'sex',
                         '#voyages']))
    return render_template("financier/guides.html", liste = liste)


@financial_bp.get('/hotels/new')
@financial_bp.post('hotels/new')
@login_required
def add_hotel():
    session['endpoint']="suppliers"
    form : HotelForm= HotelForm()
    if form.validate_on_submit():
        hotel : Hotel = Hotel()
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
        return redirect(url_for("financial_bp.hotels"))
    return render_template('financier/new_hotel.html',
                           form=form)


@financial_bp.get('/buses/new')
@financial_bp.post('buses/new')
@login_required
def add_bus():
    session['endpoint']="suppliers"
    form : BusForm= BusForm()
    if form.validate_on_submit():
        bus : Bus = Bus()
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
        return redirect(url_for("financial_bp.add_bus"))
    return render_template('financier/new_bus.html', form = form)


import os
@financial_bp.get('/guides/new')
@financial_bp.post('/guides/new')
@login_required
def add_guide():
    session['endpoint']="suppliers"
    form : GuideForm = GuideForm()
    current_dir = os.getcwd()
    # print(current_dir)
    os.chdir(current_dir + "/root/static/uploads")
    file = open("algeria_postcodes.json", "r", encoding='utf-8')
    data = json.load(file, )
    states = [(x['wilaya_name'], x['wilaya_code'] + '-' + x['wilaya_name']) for x in data]
    states = list(dict.fromkeys(states))
    os.chdir(current_dir)
    form.state.choices = states
    if form.validate_on_submit():
        guide : Guide = Guide()
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
        return redirect(url_for("financial_bp.add_guide"))
    return render_template('financier/new_guide.html', form = form)

from root.models import Subscription
@financial_bp.get('/repeal/<int:booking_id>/confirm')
@login_required
def repeal_booking(booking_id):
    session['endpoint'] = "bookings"
    booking = Subscription.query.get(booking_id)
    if not booking:
        return render_template("errors/404.html", blueprint="financial_bp"), 404

    if booking.status in ['declined','approved']:
        flash('Opération déjà validée, impossible de change le status', "danger")
        return redirect(url_for("financial_bp.repeal_booking", booking_id=booking_id))

    booking.status = 'declined'
    database.session.add(booking)
    database.session.commit()
    flash('Annulation confirmée',"success")
    return redirect(url_for("financial_bp.bookings"))



# Valider une annulation
@financial_bp.get('/supplier/payment')
@financial_bp.post('/supplier/payment')
@login_required
def supplier_payments():
    session['endpoint'] = "suppliers"
    pass

@financial_bp.get('/bookings')
@login_required
def bookings():
    session['endpoint'] = 'bookings'
    pass



@financial_bp.get('/invoices')
@login_required
def invoices():
    session['endpoint'] = 'suppliers'
    pass


@financial_bp.get('/clients')
@login_required
def clients():
    session['endpoint'] = 'bookings'
    liste = Agency.query.filter_by(is_deleted = False).all()
    liste = [
        obj.repr() for obj in liste
    ]
    return render_template("financier/clients.html", liste = liste)


@financial_bp.get('/config/edit')
@financial_bp.post('/config/edit')
@login_required
def edit_config():
    form : ConfigForm = ConfigForm()
    config : Config = Config.query.get(1)
    if form.validate_on_submit():
        config.benefice = form.benefice.data
        config.supplier_payment_period = form.supplier_payment_period.data
        config.balance_reminder = form.balance_reminder.data
        database.session.add(config)
        database.session.commit()
        flash(
            "Information ont etaient mis à jour",
            'success'
        )
        return redirect(url_for("financial_bp.index"))
    return render_template("financier/edit-config.html", form=form)


@financial_bp.get('/buses/<int:bus_id>/delete')
@login_required
def delete_bus(bus_id):
    bus = Bus.query.filter_by(is_deleted=False).get(bus_id)
    if not bus:
        return render_template('errors/404.html', blueprint="financial_bp"), 404

    # if bus.is_deleted:
    #     return render_template('errors/404.html', blueprint="financial_bp"), 404

    bus.is_deleted = True
    database.session.add(bus)
    database.session.commit()
    for contact in bus.contacts:
        database.session.delete(contact)
    database.session.commit()
    flash('Suppression se termine avec succès','success')
    return redirect(url_for("financial_bp.buses"))

@financial_bp.get('/guides/<int:guide_id>/delete')
@login_required
def delete_guide(guide_id):
    guide = Guide.query.filter_by(is_deleted=False).get(guide_id)
    if not guide:
        return render_template('errors/404.html', blueprint="financial_bp"), 404
    guide.is_deleted = True
    database.session.add(guide)
    database.session.commit()
    for contact in guide.contacts:
        database.session.delete(contact)
    database.session.commit()
    flash('Suppression se termine avec succès','success')
    return redirect(url_for("financial_bp.guides"))


@financial_bp.get('/hotels/<int:hotel_id>/delete')
@login_required
def delete_hotel(hotel_id):
    hotel = Hotel.query.filter_by(is_deleted=False).get(hotel_id)
    if not hotel:
        return render_template('errors/404.html', blueprint="financial_bp"), 404
    hotel.is_deleted = True
    database.session.add(hotel)
    database.session.commit()
    for contact in hotel.contacts:
        database.session.delete(contact)
    database.session.commit()
    flash('Suppression se termine avec succès','success')
    return redirect(url_for("financial_bp.hotels"))

