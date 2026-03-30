from  . import emp_bp
from flask import flash, redirect, url_for, render_template, session, abort, request, jsonify
from flask_login import login_required, current_user
from root.models import Trip, Guide, Bus, Departure, Subscription
from root.forms import TripForm, DepartureForm, PickUpForm
from root import database

import datetime as dt
@emp_bp.get('/trips/new')
@emp_bp.post('/trips/new')
@login_required
def add_trip():
    form: TripForm = TripForm()
    if form.validate_on_submit():
        trip = Trip()
        trip.destination = form.destination.data
        trip.nb_places = form.nb_places.data
        trip.nb_free_places = form.nb_places.data
        Trip.date_depart = form.date_depart.data
        trip.date_end=form.date_end.data
        trip.subscription_due_date = form.subscription_due_date.data
        trip.subscription_due_date += dt.timedelta(hours=23, minutes=59, seconds=59)
        trip.is_bus_included = True if form.is_bus_included.data else False
        trip.is_hotel_included = True if form.is_hotel_included.data else False
        trip.is_plane_included = True if form.is_plane_included.data else False
        trip.plane_fees= int(form.avion_fees.data) if form.avion_fees.data else None
        trip.visa_fees = int(form.visa_fees.data) if form.visa_fees.data else None
        trip.is_guide_included = True if form.is_guide_included.data else False
        trip.created_by = current_user.id
        pick_ups_list = list()
        if enumerate(form.departures):

            for d_index, d_entry in enumerate(form.departures):
                _dep = Departure()
                if d_entry.delete_entry.data:
                    del form.departures.pick_ups.entries
                    del form.departures.entries[d_index]
                    return render_template(
                        "gestionnaire/new_trip.html",
                        form=form
                    )
                if d_entry.add_pickup.data:
                    form.departures.pick_ups.append_entry()
                    return render_template(
                        "gestionnaire/new_trip.html",
                        form=form,
                        nested_pickup = PickUpForm(
                        )
                    )
                
                # Create departures and store them in a single list
                _dep.created_by = current_user.id
                # _dep.trip_id = trip.id
                _dep.date = d_entry.date.data
                _dep.state = d_entry.state.data
                _dep.nb_places = int(d_entry.nb_places.data)
                _dep.unit_price = d_entry.unit_price.data

                if enumerate(d_entry.pick_ups):
                    for pu_index, pu_entry in enumerate(d_entry.pick_ups):
                        if pu_entry.delete_entry.data:
                            del pu_entry.entries[pu_index]
                            # Create pickup and store them in a single list
                    return render_template(
                        "gestionnaire/new_trip.html",
                        form=form,
                        nested = DepartureForm()
                    )
                for pu_index, pu_entry in enumerate(d_entry.pick_ups):
                    _pu = PickUp()
                    _pu.ram_time = pu_entry.ram_time.data
                    _pu.label = pu_entry.label.data
                    _pu.x_coordinate = pu_entry.x_coordinate.data
                    _pu.y_coordinate = pu_entry.y_coordinate.data
                    _pu.map_url = pu_entry.map_url.data
                    _pu.bus_id = pu_entry.bus_id.data
                    _pu.guide_id = pu_entry.guide_id.data
                    pick_ups_list.append(dict(
                        departure=_dep,
                        pick_up=_pu
                    ))

        # add more departures
        if form.add_departure.data:
            form.departures.append_entry()
            return render_template(
                "gestionnaire/new_trip.html",
                form=form,
                nested = DepartureForm()
            )
        database.session.add(trip)
        database.session.commit()
        for entry in pick_ups_list:
            database.session.add(entry['departure'])
            for pu in entry['pick_ups']:
                pu.departure_id = entry['departure'].id
                pu.trip_id = trip.id
                database.session.add(entry['pick_up'])

        database.session.commit()
        flash('Operation terminée avec succès','success')
        return redirect(url_for("emp_bp.add_trip"))
    return render_template("gestionnaire/new_trip.html", form=form)


@emp_bp.get('/trips')
@emp_bp.get('/trips')
@login_required
def trips():
    session['endpoint'] = 'trips'
    _voyages = Trip.query.filter_by(is_deleted = False) \
                            .filter_by(created_by=current_user.id).all()
    liste = list()
    if _voyages:
        for b in _voyages:
            liste.append(b.repr(
                columns=['id',"destination","created_by","date_depart",
                         "agencies","date_end","subscription_status","places_status"]
            ))
    return render_template('gestionnaire/trips.html', liste=liste)


@emp_bp.post('/voyages/get')
@login_required
def get_voyage():
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


@emp_bp.get('/subscription/<int:voyage_id>')
@login_required
def subscriptions(voyage_id):
    voyage = Trip.query.get(voyage_id)
    if not voyage or Trip.is_deleted==True:
        return render_template("errors/404.html", blueprint="emp_bp")
    v_for_a = Subscription.query.filter_by(fk_voyage_id = voyage_id).all()
    if not v_for_a:
        return render_template("errors/404.html", blueprint="emp_bp")

    return render_template("gestionnaire/voyage_subscriptions.html",
                           object=voyage.repr(columns=['destination','id','agencies']))


@emp_bp.get("/trip/<int:voyage_id>/delete")
@login_required
def delete_trip(voyage_id):
    """Delete trip"""
    voyage = Trip.query.get(voyage_id)
    if not voyage:
        return render_template("errors/page-404.html", blueprint="emp_bp")
    if voyage.created_by != current_user:
        abort(403)
    voyage.is_deleted=True
    database.session.add(voyage)
    database.session.commit()
    flash('Suppression avec succès', 'success')
    return redirect(url_for("emp_bp.voyages"))


@emp_bp.get("/trips/<int:trip_id>/departures")
@login_required
def departures(trip_id):
    """List departures for a given trip"""
    trip = Trip.query.get(trip_id)
    if not trip:
        abort(404)

    if trip.created_by != current_user:
        flash('Operation non autorisée')
        abort(403)

    l_departures = Departure.query.filter(Departure.trip_id == trip_id).all()
    if not l_departures:
        flash('Aucun départ pour ce voyage',"danger")
        abort(404)

    return jsonify(
        data={
             depart.to_dict() for depart in l_departures
         }
    ), 200


@emp_bp.get('/trips/<int:trip_id>/departures/<int:depart_id>/delete')
@login_required
def departures_delete(trip_id, depart_id):
    """Delete departure"""
    trip = Trip.query.get(trip_id)
    if not trip:
        abort(404)

    if trip.created_by != current_user:
        flash('Operation non autorisée')
        abort(403)

    depart = Departure.query.get(depart_id)
    if trip.id != depart.trip_id:
        # flash('Aucun départ pour ce voyage', "danger")
        abort(403)

    database.session.delete(depart)
    database.session.commit()
    return jsonify(
        message="Objet supprimé avec succès"
    ), 200


# @emp_bp.get("/trips/<int:trip_id>/departures/create")
# @emp_bp.post('/trips/<int:trip_id>/departures/create')
# @login_required
# def create_departure(voyage_id):
#     """Add departure"""
#     pass

from root.models import PickUp
@emp_bp.get("/trips/<int:trip_id>/pickupPoints")
# @emp_bp.post("/trips/<int:voyage_id>/departures")
@login_required
def pickups_points(trip_id):
    """Pickup points for a given trip"""
    trip = Trip.query.get(trip_id)
    if not trip:
        abort(404)

    if trip.created_by != current_user:
        # flash('Operation non autorisée')
        abort(403)

    pickups = PickUp.query.filter(Departure.trip_id == trip_id).all()
    if not pickups:
        # flash('Aucun départ pour ce voyage', "danger")
        abort(404)

    return jsonify(
        message="success",
        data={
            pup.to_dict() for pup in pickups
        }
    ), 200


@emp_bp.get('/trips/<int:trip_id>/pickupPoints/<int:pickup_id>/delete')
@login_required
def pickup_delete(trip_id, pickup_id):
    """Delete pickup"""
    trip = Trip.query.get(trip_id)
    if not trip:
        abort(404)

    if trip.created_by != current_user:
        flash('Operation non autorisée')
        abort(403)

    pickup = PickUp.query.get(pickup_id)
    if trip.id != pickup.trip_id:
        # flash('Aucun départ pour ce voyage', "danger")
        abort(403)

    database.session.delete(pickup)
    database.session.commit()
    return jsonify(
        message="Objet supprimé avec succès"
    ), 200


# @emp_bp.get("/trips/<int:trip_id>/pickupPoints/create")
# @emp_bp.post('/trips/<int:trip_id>/pickupPoints/create')
# @login_required
# def create_pickup(trip_id):
#     """Add pickup"""
#     pass


