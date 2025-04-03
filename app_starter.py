import datetime as dt

from flask_migrate import Migrate
from sqlalchemy.sql.operators import or_, and_

from root import create_app,database
from flask import redirect, url_for
import os
from root.models import *
from dotenv import load_dotenv
from root import scheduler

load_dotenv('.env')
app = create_app(os.environ.get('FLASK_ENV'))
app.config.update(dict(
        MAIL_USERNAME=os.environ.get('MAIL_USERNAME'),
        MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ))
migrate = Migrate(app=app, db=database)
moment_to_trigger = dt.datetime.now()+dt.timedelta(seconds=120)

def update_database():
    with app.app_context():
        voyages = Voyage.query.filter(and_(Voyage.is_deleted == False,
                                           or_(Voyage.is_submitted_for_payment == False,
                                               Voyage.is_submitted_for_payment == None)))\
                                .filter(Voyage.subscription_due_date<moment_to_trigger).all()
        if len(voyages)>0:
            for v in voyages:
                participants = v.nb_places - v.nb_free_places
                if participants!=0:
                    hotels = Voyage.query.get(v.id).hotels_fees if v.is_hotel_included==True else 0
                    bus = Voyage.query.get(v.id).bus_fees if v.is_bus_included==True else 0
                    guide = Voyage.query.get(v.id).guide_fees if v.is_guide_included==True else 0
                    visa = Voyage.query.get(v.id).visa_fees if v.is_visa_included==True else 0
                    plane = Voyage.query.get(v.id).plane_fees if v.is_plane_included==True else 0

                    benefice = (Config.query.get(1).benefice/100)
                    prix_total_achat = hotels+bus+guide+(visa*participants)+(plane*participants)
                    total_vente_total = prix_total_achat*(1+benefice)
                    price_per_place=total_vente_total/participants
                    for a in v.agencies:
                        try:
                            v_for_a = VoyageForAgency.query.filter(and_(VoyageForAgency.fk_voyage_id==v.id,VoyageForAgency.fk_agency_id==a.id)).first()
                            if v_for_a:
                                v_for_a.rest_to_pay=a.reserved_places*price_per_place
                                v_for_a.total_paid=0
                                database.session.add(v_for_a)
                                database.session.commit()

                        except Exception as e:
                            database.session.rollback()
                    v.is_submitted_for_payment=True
                    database.session.add(v)
                    database.session.commit()

with app.app_context():
    # voyages = Voyage.query.filter(and_(Voyage.is_deleted == False, or_(Voyage.is_submitted_for_payment == False, Voyage.is_submitted_for_payment==None))) \
    #     .filter(Voyage.subscription_due_date < moment_to_trigger).all()
    # for v in voyages:
    #     print(v.subscription_due_date)
    scheduler.add_job(id=f"calculer_prix_voyage", func=update_database,
                      trigger="date", run_date=dt.datetime.now())

@app.route('/')
def index():
    return redirect(url_for('auth_bp.login'))

@app.shell_context_processor
def make_shell_context():
    return dict(app=app,
                db=database
                )
