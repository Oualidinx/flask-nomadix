from root import database as db
from flask_login import UserMixin, current_user
from datetime import datetime
import json


class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime):
            return str(z)
        else:
            return super().default(z)


class Config(db.Model):
    __tablename__ = "config"
    id = db.Column(db.Integer, primary_key=True)
    benefice = db.Column(db.Float, nullable=False)
    supplier_payment_period=db.Column(db.Float, default = 15) # days
    balance_reminder = db.Column(db.Float, default = 7) # days
    cancellation_fee = db.Column(db.Float, default = 0)


class User(UserMixin, db.Model):
    __tablename__="user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    role = db.Column(db.String(20))
    is_deleted = db.Column(db.Boolean, default=0)
    password_hasChanged = db.Column(db.Boolean, default = False)
    username = db.Column(db.String(100), nullable = False)
    phone_number = db.Column(db.String(10), default="champ vide")
    password_hash = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f'USER: <{self.username}, {self.first_name}, {self.last_name}> \n'

    def repr(self, columns=None):
        _dict = {
            'id': self.id,
            'full_name': self.first_name+" "+self.last_name,
            'username': self.username,
            'role': self.role,
            'phone_number': self.phone_number
        }
        return {key: _dict[key] for key in columns} if columns else _dict


class Trip(db.Model):
    __tablename__="trip"
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(100))
    is_deleted = db.Column(db.Boolean, default=0)
    is_submitted_for_payment=db.Column(db.Boolean, default = 0)
    subscription_due_date=db.Column(db.DateTime, default=datetime.now())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_depart = db.Column(db.DateTime, default=datetime.utcnow)
    date_end = db.Column(db.DateTime, default=datetime.utcnow)
    hotel_fees = db.Column(db.Integer, default=0)
    nb_places = db.Column(db.Integer, default = 0)
    nb_free_places = db.Column(db.Integer, default = 0)
    bus_fees = db.Column(db.Integer, default=0)
    visa_fees = db.Column(db.Integer, default=0)
    guide_fees = db.Column(db.Integer, default=0)
    plane_fees = db.Column(db.Integer, default=0)
    is_plane_included = db.Column(db.Boolean, default=0)
    is_guide_included = db.Column(db.Boolean, default=0)
    is_hotel_included = db.Column(db.Boolean, default=0)
    is_bus_included = db.Column(db.Boolean, default=0)
    is_visa_included = db.Column(db.Boolean, default=0)
    # includes = db.relationship('Include', backref="travel_include", lazy="subquery")
    # agencies = db.relationship("Agency", secondary="trip_agency",
    #                            viewonly=True,
    #                         primaryjoin="trip.id==foreign(TripForAgency.fk_trip_id)",
    #                         secondaryjoin="Agency.id==foreign(TripForAgency.fk_agency_id)")

    # invoices = db.relationship('Invoice', backref="trip_invoices", lazy="subquery")
    departures = db.relationship('Departure',backref="trip_departures", lazy='subquery')
    confirmed_bookings = db.relationship('Booking',
                                         viewonly=True,
                                         primaryjoin="and_(Booking.fk_trip_id == Trip.id, Booking.is_confirmed)")
    cancelled_bookings = db.relationship('Booking',
                                         backref="cancelled_trip_bookings",
                                         primaryjoin = "and_(Booking.fk_trip_id==Trip.id, Booking.status=='cancelled')", viewonly=True)
    pending_bookings = db.relationship('Booking',
                                       backref="pending_trip_bookings",
                                       primaryjoin="and_(Booking.fk_trip_id==Trip.id, "
                                                      "Booking.status=='pending')",
                                       viewonly=True)

    def repr(self, columns=None, columns_for_agencies=None, columns_for_persons=None):
        _dict={
            "id": self.id,
            "destination": self.destination,
            "created_at":self.created_at,
            "created_by":User.query.get(self.created_by).first_name+" "+User.query.get(self.created_by).last_name,
            "date_depart":self.date_depart.date(),
            "subscription_due_date":self.subscription_due_date.date(),
            "date_end":self.date_end.date(),
            "nb_places":self.nb_places,
            "nb_free_places":self.nb_free_places,
            # "hotel_fees":"{:,.2f}".format(self.hotel_fees) if self.is_hotel_included else 0,
            # "bus_company": Bus.query.get(self.includes[0].fk_bus_id) if len(self.includes)>0 and self.includes[0].fk_bus_id else "",
            # "bus_fees":"{:,.2f}".format(self.bus_fees) if self.is_bus_included else 0,
            # "visa_fees":"{:,.2f}".format(self.visa_fees) if self.is_visa_included else 0,
            # "guide_fees":"{:,.2f}".format(self.guide_fees) if self.is_guide_included else 0,
            # "guide_full_name":Guide.query.get(self.includes[0].fk_guide_id) if len(self.includes) > 0 and self.includes[0].fk_guide_id else "",
            # "hotel_name":Hotel.query.get(self.includes[0].fk_hotel_id) if len(self.includes) > 0 and self.includes[0].fk_hotel_id else "",
            # "plane_fees":"{:,.2f}".format(self.plane_fees) if self.is_plane_included else 0,
            "is_plane_included":"inclue" if self.is_plane_included else "exclu",
            "is_guide_included":"inclue" if self.is_guide_included else "exclu",
            "is_hotel_included":"inclue" if self.is_hotel_included else "exclu",
            "is_bus_included":"inclue" if self.is_bus_included else "exclu",
            "is_visa_included":"inclue" if self.is_visa_included else "exclu",
            "agencies":[agency.repr(columns=columns_for_agencies, columns_for_persons=columns_for_persons) for agency in self.agencies] if len(self.agencies)>0 else None,
            "subscription_status": ("#A6001A","Inscriptions fermées") if self.subscription_due_date < datetime.now() else None,
            "places_status": ("#A6001A","Nombre de places atteint la limite") if self.nb_free_places == 0 else None,
        }
        return {key: _dict[key] for key in columns} if columns else _dict


class Bus(db.Model):
    __tablename__="bus"
    id=db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100))
    driver_full_name = db.Column(db.String(100))
    capacity = db.Column(db.Integer)
    state = db.Column(db.String(100), nullable = True)
    is_deleted = db.Column(db.Boolean, default=0)
    contacts = db.relationship('Contact', backref="bus_contact", lazy='subquery')
    # trips = db.relationship('Trip', secondary="include",viewonly=True,
    #                         primaryjoin="Bus.id == foreign(Include.fk_bus_id)",
    #                         secondaryjoin="Trip.id == foreign(Include.fk_trip_id)")
    def __repr__(self):
        return f'{self.company}'

    def repr(self, columns=None):
        _dict = {
            'id': self.id,
            'driver_full_name': self.driver_full_name,
            'capacity': self.capacity,
            'state':self.state,
            'company': self.company,
            'contacts': [contact.repr(['phone']) for contact in self.contacts]
        }
        return {key: _dict[key] for key in columns} if columns else _dict


class Contact(db.Model):
    __tablename__ =  "contact"
    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    address = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    is_deleted = db.Column(db.Boolean, default=0)
    fk_bus_id = db.Column(db.Integer, db.ForeignKey('bus.id'))
    fk_guide_id = db.Column(db.Integer, db.ForeignKey('guide.id'))
    fk_hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'))
    fk_agency_id = db.Column(db.Integer, db.ForeignKey('agency.id'))
    fk_person_id = db.Column(db.Integer, db.ForeignKey('person.id'))

    def __repr__(self):
        return (f'Contact: {self.name}, '
                f'email={self.email}, '
                f'phone={self.phone}, '
                f'address={self.address}'
                f'city={self.city}, '
                f'state={self.state}, '
                f'is_deleted={self.is_deleted}')

    def repr(self, columns=None):
        _dict = {
                'name': self.name,
                'email': self.email,
                'phone':self.phone,
                'address':self.address,
                'city':self.city,
                'state':self.state,
                'is_deleted':self.is_deleted}
        return {key: _dict[key] for key in columns} if columns else _dict


class Guide(db.Model):
    __tablename__ = "guide"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    is_deleted = db.Column(db.Boolean, default=False)
    picture = db.Column(db.String(1500))
    sex = db.Column(db.String(10))
    state = db.Column(db.String(100), nullable=True)
    contacts = db.relationship('Contact', backref="guide_contact", lazy='subquery')
    trips = db.relationship('Trip', secondary="pickup",viewonly=True,
                            primaryjoin="Guide.id == foreign(PickUp.fk_guide_id)",
                            secondaryjoin="Trip.id == foreign(PickUp.fk_trip_id)")

    def __repr__(self):
        return f'{self.name}'

    def repr(self, columns=None):
        _dict = {
            'id':self.id,
            'name': self.name,
            'sex': self.sex,
            'state':self.state,
            '#trips': len(self.trips),
            'trips':self.trips,
            'contacts':[c.repr() for c in self.contacts]
        }
        return {key: _dict[key] for key in columns} if columns else _dict


class Hotel(db.Model):
    __tablename__ = "hotel"
    id = db.Column(db.Integer, primary_key=True)
    is_deleted = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(100))
    contacts = db.relationship('Contact', backref="hotel_contact", lazy='subquery')
    star_rating = db.Column(db.Integer, default=0)
    state = db.Column(db.String(100))
    trips = db.relationship('Trip', secondary="room_price", viewonly=True,
                              primaryjoin="Hotel.id == foreign(RoomPrice.fk_hotel_id)",
                              secondaryjoin="and_(Trip.id == foreign(Booking.fk_trip_id), "
                                            "RoomPrice.id == foreign(Booking.fk_price_id))")
    prices = db.relationship('RoomPrice',
                             backref="hotel_room_prices", 
                             lazy="subquery")


    def __repr__(self):
        return f'{self.name}'

    def repr(self, columns=None):
        _dict = {
            'id': self.id,
            'name': self.name,
            'is_deleted': self.is_deleted,
            'star_rating': self.star_rating,
            "#trips":len(self.trips) if len(self.trips)>0 else 0,
            "trips":[v.repr() for v in self.trips],
            'contacts': [c.repr(['phone'])['phone'] for c in self.contacts]
        }
        return {key: _dict[key] for key in columns} if columns else _dict


# un group de person (agences) ou un seul client (indivduels)
class Agency(db.Model):
    __tablename__ = "agency"
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100))
    responsible_full_name = db.Column(db.String(100))
    code_grp = db.Column(db.String(50), nullable=False, default="G/")
    created_at=db.Column(db.DateTime, default=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=0)
    reserved_places= db.Column(db.Integer, default=0)
    contacts = db.relationship('Contact', backref="agency_contact", lazy='subquery')
    persons = db.relationship('Person', backref="agency_persons", lazy="subquery")
    invoice = db.relationship('Invoice', backref="agency_invoice", lazy="subquery")

    def __repr__(self):
        return f'{self.label}, Responsable: {self.responsible_full_name}, Contacts: {self.contacts}'

    def repr(self, columns=None, columns_for_persons=None):
        _dict = {
            'id':self.id,
            'label': self.label,
            'created_at': self.created_at,
            'responsible_full_name': self.responsible_full_name,
            'is_deleted': self.is_deleted,
            'code_group':self.code_grp if self.code_grp else "No code yet",
            'reserved_places': self.reserved_places,
            'contacts':self.contacts[0].repr(['phone'])['phone'],
            'persons':[p.repr(columns_for_persons) for p in self.persons]
            # 'invoice':self.invoice.repr()
        }
        return {c:_dict[c] for c in columns} if columns else _dict


class Invoice(db.Model):
    __tablename__ = "invoice"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Integer)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    payments = db.relationship('Payment', backref='payments_invoice', lazy='subquery')
    # fk_trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'))
    fk_agency_id = db.Column(db.Integer, db.ForeignKey('agency.id'))
    invoice_type = db.Column(db.String(100))
    entities = db.relationship('Entity', backref='invoice_entities', lazy='subquery')

    def __repr__(self):
        return (f'Date de facture={self.date},'
                f'Montant= {self.amount}, '
                f'trip={Trip.query.get(self.fk_trip_id)},'
                f'Agency={Agency.query.get(self.fk_agency_id)}, '
                f'Payments={self.payments}')


class Payment(db.Model):
    __tablename__ = "payment"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    created_by=db.Column(db.Integer, db.ForeignKey('user.id'))
    amount = db.Column(db.Integer)
    type = db.Column(db.String(100))
    fk_invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'))

    def __repr__(self):
        return f'Date de payment={self.date}, Montant={self.amount}'

    def repr(self, columns=None):
        _dict = {
            'id': self.id,
            'date': self.date,
            'id_invoice':Invoice.query.get(self.fk_invoice_id).code if self.fk_invoice_id and Invoice.query.get(self.fk_invoice_id) else "/",
            'id_transaction':self.code,
            'id_trip':Trip.query.get(Invoice.query.get(self.fk_invoice_id).trip_id).id
                                if self.fk_invoice_id and Trip.query.get(Invoice.query.get(self.fk_invoice_id).trip_id)
                                   and Trip.query.get(Invoice.query.get(self.fk_invoice_id).trip_id).is_deleted==0 else "/",
            'client_full_name':"",
            'amount':"{:,.2f}".format(self.amount),
        }
        return {key: _dict[key] for key in columns} if columns else _dict


class Person(db.Model):
    __tablename__ = "person"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    is_deleted = db.Column(db.Boolean, default=0)
    sexe = db.Column(db.String(1))

    contacts = db.relationship('Contact', backref="person_contact", lazy='subquery')
    fk_agency_id = db.Column(db.Integer, db.ForeignKey('agency.id'))

    def repr(self, columns=None):
        _dict={
            'id':self.id,
            'first_name':self.first_name,
            'last_name':self.last_name,
            'sexe':self.sexe,
            'is_deleted':self.is_deleted,
            'contacts':self.contacts[0].repr(['phone'])['phone'],
        }
        return {c:_dict[c] for c in columns} if columns else _dict


# class Include(db.Model):
#     __tablename__ = "include"
#     id = db.Column(db.Integer, primary_key=True)
#     fk_trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'))
#     # fk_guide_id = db.Column(db.Integer, db.ForeignKey('guide.id'))
#     # fk_bus_id = db.Column(db.Integer, db.ForeignKey('bus.id'))
#     price_id = db.Column(db.Integer, db.ForeignKey('room_price.id'))


class RoomPrice(db.Model):
    __tablename__ = "room_price"
    id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.String(10))
    price = db.Column(db.Double, default = 0)
    fk_hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'))


class Booking(db.Model):
    __tablename__ = "booking"
    id = db.Column(db.Integer, primary_key=True)
    fk_agency_id = db.Column(db.Integer, db.ForeignKey('agency.id')) # Client
    fk_trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'))
    total_to_pay=db.Column(db.Double, default = 0)
    rest_to_pay=db.Column(db.Double, default = 0)
    """
    status: describes the status of the subscription cancellation process
    two options:
    * pending : Accountant does not review the pending cancellation yet',
    * confirmed: Accountant accepted the cancellation
    * rejected: Accountant rejected the cancellation
    """
    status = db.Column(db.String(15), default = "")
    """
    Does the client pay all the booking fees
    """
    is_confirmed = db.Column(db.Boolean, default=False)

    refund = db.Column(db.Double, default = 0)
    fk_price_id  = db.Column(db.Integer, db.ForeignKey('room_price.id'))


    def __repr__(self, query = None):
        if query:
            return f"Groupe= {Agency.query.get(self.fk_agency_id).label} , trip = {query.get(self.fk_trip_id).destination}"
        return f"Groupe= {Agency.query.get(self.fk_agency_id).label} , trip = {Trip.query.get(self.fk_trip_id).destination}"

    def repr(self, query = None, columns_booking=None, columns_trip=None, columns_agency=None):
        if query:
            trip_dict = query.filter_by(id = self.fk_trip_id).first().repr(columns_trip)
        else:
            trip_dict = Trip.query.filter_by(id = self.fk_trip_id).first().repr(columns_trip)

        group_dict = Agency.query.get(self.fk_agency_id).repr(columns_agency)

        booking_dict = {
            'cancellation_status': self.status,
            'total_to_pay': self.total_to_pay,
            'rest_to_pay': self.rest_to_pay,
            'room_price': self.fk_price_id, # Room price
            'refund':self.refund,
            'confirmed':self.is_confirmed,
        }
        if columns_booking:
            booking_dict = {**booking_dict, **columns_booking}
        group_dict.update(trip_dict)

        return booking_dict.update(group_dict)


class Entity(db.Model):
    __tablename__ = "entity"
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100))
    is_deleted = db.Column(db.Boolean, default=0)
    montants = db.Column(db.Integer)
    unit = db.Column(db.String(100))
    quantity = db.Column(db.Integer, default=1)
    total_amount = db.Column(db.Integer,default=0)
    fk_invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'))

    def __repr__(self):
        return f'{self.label}, {self.montants}, {self.unit}, {self.quantity}, {self.total_amount}'

class Departure(db.Model):
    __tablename__ = "departure"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable = False)
    state = db.Column(db.String(150))
    nb_places = db.Column(db.Integer, default = 0)
    unit_price = db.Column(db.Numeric(precision = 10 , scale = 2), default = 0)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'))

    def to_dict(self):
        return dict(
            id=self.id,
            date=self.date.strftime("%Y-%m-%d"),
            nb_places=self.nb_places,
            unit_price=self.unit_price,
            created_by=f'{User.query.get(self.created_by).first_name} {User.query.get(self.created_by).last_name}',
            trip_id=Trip.query.get(self.trip_id).destination or "NA"
        )

class PickUp(db.Model):
    __tablename__ = "pickup"
    id = db.Column(db.Integer, primary_key = True)
    ram_time = db.Column(db.Time, nullable = False)
    label = db.Column(db.String(150))
    x_coordinate = db.Column(db.Double, default = 0)
    y_coordinate = db.Column(db.Double, default = 0)
    map_url = db.Column(db.String(150), nullable = True)
    fk_bus_id = db.Column(db.Integer, db.ForeignKey('bus.id'))
    fk_guide_id = db.Column(db.Integer, db.ForeignKey('guide.id'))
    fk_departure_id = db.Column(db.Integer, db.ForeignKey('departure.id'))
    fk_trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'))

    def to_dict(self):
        return dict(
            id=self.id,
            ram_datetime=self.ram_datetime.strftime("%Y-%m-%d"),
            label=self.label,
            state=self.state,
            x_coordinate=self.x_coordinate,
            y_coordinate=self.y_coordinate,
            bus_id=Bus.query.get(self.bus_id).label,
            guide_id=Guide.query.get(self.guide_id).name,
            departure=self.departure.to_dict(),
            trip_id=Trip.query.get(self.trip_id).destination,
        )