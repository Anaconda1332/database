from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Tenant, RentingPerson, PaymentMethod, Booking, Review, Housing, Address
from sqlalchemy.sql import text

DATABASE_URL = "postgresql://postgres:Dolphin20@localhost/airbnb"
engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)
session = Session()

def delete_users(session):
    session.query(User).delete()
    session.commit()

def delete_tenants(session):
    session.query(Tenant).delete()
    session.commit()

def delete_renting_persons(session):
    session.query(RentingPerson).delete()
    session.commit()

def delete_payment_methods(session):
    session.query(PaymentMethod).delete()
    session.commit()

def delete_bookings(session):
    session.query(Booking).delete()
    session.commit()

def delete_reviews(session):
    session.query(Review).delete()
    session.commit()

def delete_housings(session):
    session.query(Housing).delete()
    session.commit()

def delete_addresses(session):
    session.query(Address).delete()
    session.commit()

def reset_user_sequence(session):
    session.execute(text('ALTER SEQUENCE users_user_id_seq RESTART WITH 1'))
    session.commit()

def reset_tenant_sequence(session):
    session.execute(text('ALTER SEQUENCE tenants_ten_id_seq RESTART WITH 1'))
    session.commit()

def reset_renting_person_sequence(session):
    session.execute(text('ALTER SEQUENCE renting_persons_ranting_id_seq RESTART WITH 1'))
    session.commit()

def reset_payment_method_sequence(session):
    session.execute(text('ALTER SEQUENCE payment_methods_pay_id_seq RESTART WITH 1'))
    session.commit()

def reset_booking_sequence(session):
    session.execute(text('ALTER SEQUENCE bookings_booking_id_seq RESTART WITH 1'))
    session.commit()

def reset_review_sequence(session):
    session.execute(text('ALTER SEQUENCE reviews_review_id_seq RESTART WITH 1'))
    session.commit()

def reset_housing_sequence(session):
    session.execute(text('ALTER SEQUENCE housings_housing_id_seq RESTART WITH 1'))
    session.commit()

def reset_address_sequence(session):
    session.execute(text('ALTER SEQUENCE addresses_address_id_seq RESTART WITH 1'))
    session.commit()

# Удаление всех записей из таблиц
delete_reviews(session)
delete_bookings(session)
delete_housings(session)
delete_renting_persons(session)
delete_payment_methods(session)
delete_tenants(session)
delete_users(session)
delete_addresses(session)

reset_user_sequence(session)
reset_tenant_sequence(session)
reset_renting_person_sequence(session)
reset_payment_method_sequence(session)
reset_booking_sequence(session)
reset_review_sequence(session)
reset_housing_sequence(session)
reset_address_sequence(session)