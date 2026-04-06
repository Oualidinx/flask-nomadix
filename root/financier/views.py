import json

from flask import render_template, flash, redirect, url_for, request, jsonify, abort
from . import financial_bp
from flask_login import login_required

from root import database
from root.forms import HotelForm, GuideForm, BusForm, ConfigForm
from root.models import Hotel, Contact, Guide, Bus, Agency, Config, Trip
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
                         "#trips"]))
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
    return render_template("financier/buses.html",
                           liste = liste)


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
                         '#trips']))
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


@financial_bp.get('/bookings/decline_requests')
@login_required
def decline_requests():
    return redirect(url_for("financier_bp.trips"))


from root.models import Booking
@financial_bp.get('/bookings/<int:booking_id>/decline/confirm')
@login_required
def decline_booking(booking_id):
    session['endpoint'] = "bookings"
    booking = Booking.query.get(booking_id)
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
    return render_template("financier/payments.html")


@financial_bp.get('/trips/bookings/<int:trip_id>/<string:q>')
@login_required
def bookings(trip_id, q=None):
    session['endpoint'] = 'bookings'
    if not trip_id:
        abort(400)

    trip = Trip.query.get(trip_id)
    if not trip:
        abort(404)

    if trip.is_deleted:
        abort(404)

    query=Booking.query.filter_by(trip_id=trip.id)

    if q is None or q=="all":
        # query = all_bookings
        list_booking = [
            response.repr(query)
            for response in query.all()
        ]
        return render_template('financier/bookings.html',
                               liste=list_booking)

    if q == 'pending':
        query = query.filter(Booking.status=="pending")# Pending cancellation
        list_booking = [
            response.repr(query)
            for response in query.all()
        ]
        return render_template('financier/bookings.html',
                               liste=list_booking)
    if q == "confirmed":
        query = query.filter(Booking.status=="confirmed")
        list_booking = [
            response.repr(query)
            for response in query.all()
        ]
        return render_template('financier/bookings.html',
                               liste=list_booking)

    if q == "rejected":
        query = query.filter(Booking.status == "rejected")
        list_booking = [
            response.repr(query)
            for response in query.all()
        ]
        return render_template('financier/bookings.html',
                               liste=list_booking)
    abort(400)


@financial_bp.get('/bookings/<int:booking_id>')
@login_required
def get_booking(booking_id):
    """
    Display a modal that contains all information about such a booking object
    booking_id: targeted booking id
    """
    booking = Booking.query.get(booking_id)
    if not booking:
        abort(404)

    # Return rendered HTML partial
    html = render_template('modals/booking_detail.html',
                           booking=booking.repr(columns_booking=['status',
                                                                 'total_to_pay',
                                                                 'rest_to_pay']))
    return jsonify({'html': html})

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
    bus = Bus.query.filter_by(is_deleted=False).filter_by(id=bus_id).first()
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
    guide = Guide.query.filter_by(is_deleted=False).filter_by(id=guide_id).first()
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
    hotel = Hotel.query.filter_by(is_deleted=False).filter_by(id=hotel_id).first()
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


@financial_bp.get('/trips')
@login_required
def trips():
    _trips = Trip.query.filter_by(is_deleted=False).all()
    liste = list()
    if _trips:
        for b in _trips:
            liste.append(b.repr(
                columns=['id', "destination", "created_by", "date_depart",
                         "agencies", "date_end", "subscription_status", "places_status"]
            ))
    return render_template(
        "financier/trips.html",
                           liste = liste)



@financial_bp.get('/buses/<int:bus_id>/view')
@login_required
def get_bus(bus_id):
    session['endpoint'] = 'buses'

    # data = request.json
    b = Bus.query.get(bus_id)
    if not b:
        abort(404)

    if b.is_deleted:
        abort(404)
    # contacts_str = ""
    # i=1
    # for c in b.contacts:
    #     contacts_str += (f"<span>        </span>{i} - <span class='fw-bold mb-3'>Nom: {c.name}</span> <br> "
    #                      f"<span>               </span><span class='fw-bold mb-3'>Numéro de téléphone: {c.phone}</span> <br>\n")
    #     i+=1
    # return jsonify(message=f"<h4 class='h4 fw-bold'>{b.company}</h4> \
    #                     <span class='fw-bold mb-3'>Conducteur: </span>{b.driver_full_name} <br> \
    #                     <span class='fw-bold mb-3'>Nombre de places: </span>{b.capacity} <br> \
    #                     <span class='fw-bold mb-3'>Contacts: </span> <br>"+contacts_str
    #                            ), 200
    return jsonify({
        'html': render_template("modals/bus-details.html",
                                bus = b.repr())
    })



@financial_bp.get('/guides/<int:guide_id>/view')
@login_required
def get_guide(guide_id):
    session['endpoint'] = 'suppliers'

    # data = request.json
    b = Guide.query.get(guide_id)
    if not b:
        abort(404)

    if b.is_deleted:
        abort(404)

    html =render_template("modals/guide.html",
                          guide = b.repr())
    # print(b.repr())
    return jsonify({
        'html': html
    })


@financial_bp.get('/hotels/<int:hotel_id>/view')
@login_required
def get_hotel(hotel_id):
    print('called')
    session['endpoint'] = 'hotels'
    # data = request.json
    hotel = Hotel.query.get(hotel_id)
    if not hotel:
        abort(404)

    if hotel.is_deleted:
        abort(404)

    # contacts_str = ""
    # i=1
    # for c in b.contacts:
    #     contacts_str += (f"<span>        </span>{i}) <span class='fw-bold mb-3'>Nom:</span> {c.name}  "
    #                      f"<br><span style=\"color:white;\">....</span><span class='fw-bold mb-3'>Numéro de téléphone: </span> {c.phone} <br>\n")
    #     i+=1
    # return jsonify(message=f"<h4 class='h4 fw-bold'>Hôtel {b.name}</h4>"
    #                        f"<span class='fw-bold mb-3'>Classement par étoiles: </span>{b.repr(['star_rating'])['star_rating']} étoiles(s)<br>"
    #                        f"<span class='fw-bold mb-3'>Contacts: </span> <br>" + contacts_str), 200
    print(hotel.repr())
    html = render_template('modals/hotel_details.html',
                           hotel=hotel.repr())

    return jsonify({'html': html})


@financial_bp.get('/trips/get')
@login_required
def get_trip():
    session['endpoint'] = 'trips'
    data = request.json
    v = Trip.query.get(int(data['voyage_id']))
    if not v:
        abort(404)
    _dict = v.repr()
    return jsonify(
        message=f"<h3 class='h3 fw-bold'>Excursion vers {_dict['destination']}</h3>"
                f"<span class='fw-bold mb-3'> Date de départ: </span>{_dict['date_depart']}<br>"
                f"<span class='fw-bold mb-3'> Date de retour: </span>{_dict['date_end']}<br>"
                f"<span class='fw-bold mb-3'> Date de clôture des inscriptions: </span>{_dict['subscription_due_date']}<br>"
                f"<span class='fw-bold mb-3'> Bus: </span>{_dict['is_bus_included']}<br>"
                f"<span class='fw-bold mb-3'> Companie de bus: </span>{_dict['bus_company']}<br>"
                f"<span class='fw-bold mb-3'> Guide: </span>{_dict['is_guide_included']}<br>"
                f"<span class='fw-bold mb-3'> Nom du guide: </span>{_dict['guide_full_name']}<br>"
                f"<span class='fw-bold mb-3'> Hôtel: </span>{_dict['is_hotel_included']}<br>"
                f"<span class='fw-bold mb-3'> Nom de l'hôtel: </span>{_dict['hotel_name']}<br>"
                f"<span class='fw-bold mb-3'> Avion: </span>{_dict['is_plane_included']}<br>"
                f"<span class='fw-bold mb-3'> Visa: </span>{_dict['is_visa_included']}<br>"
                f"<span class='fw-bold mb-3'> Nombre des inscrits: </span>{_dict['nb_places']-_dict['nb_free_places']}<br>"
    ), 200


@financial_bp.post('/trips/<int:trip_id>/delete')
@login_required
def delete_trip(trip_id):
    trip = Trip.query.get(trip_id)
    if not trip:
        abort(404)

    if len(trip.pending_bookings)>0:
        flash('Opération impossible: des demandes d\'annulation en attente de réponses',"warning")
        return redirect(url_for('financial_bp.trips'))

    if trip.is_deleted:
        abort(404)
    trip.is_deleted = True
    database.session.add(trip)
    database.session.commit()
    flash('Suppression avec succès',"success")
    return redirect(url_for('financial_bp.trips'))
