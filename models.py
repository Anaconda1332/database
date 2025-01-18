from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    contact = Column(String(50), nullable=False)
    bio = Column(String(500), nullable=True)
    date_of_birth = Column(Date, nullable=False)

    tenant = relationship("Tenant", uselist=False, back_populates="user")
    renting_person = relationship("RentingPerson", uselist=False, back_populates="user")

class Tenant(Base):
    __tablename__ = 'tenants'

    ten_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), unique=True, nullable=True)

    user = relationship("User", back_populates="tenant")
    payment_methods = relationship("PaymentMethod", back_populates="tenant")
    bookings = relationship("Booking", back_populates="tenant")
    reviews = relationship("Review", back_populates="tenant")

class RentingPerson(Base):
    __tablename__ = 'renting_persons'

    ranting_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), unique=True, nullable=True)

    user = relationship("User", back_populates="renting_person")
    housings = relationship("Housing", back_populates="renting_person")

class PaymentMethod(Base):
    __tablename__ = 'payment_methods'

    pay_id = Column(Integer, primary_key=True, autoincrement=True)
    ten_id = Column(Integer, ForeignKey('tenants.ten_id'), nullable=False)
    pin = Column(String(4), nullable=False)
    number_of_card = Column(String(50), nullable=False)
    bank = Column(String(50), nullable=False)

    tenant = relationship("Tenant", back_populates="payment_methods")

class Booking(Base):
    __tablename__ = 'bookings'

    booking_id = Column(Integer, primary_key=True, autoincrement=True)
    ten_id = Column(Integer, ForeignKey('tenants.ten_id'), nullable=False)
    housing_id = Column(Integer, ForeignKey('housings.housing_id'), nullable=False)
    departure_date = Column(Date, nullable=False)
    number_of_guests = Column(Integer, nullable=False)
    check_in_date = Column(Date, nullable=False)

    tenant = relationship("Tenant", back_populates="bookings")
    housing = relationship("Housing", back_populates="bookings")

class Review(Base):
    __tablename__ = 'reviews'

    review_id = Column(Integer, primary_key=True, autoincrement=True)
    ten_id = Column(Integer, ForeignKey('tenants.ten_id'), nullable=False)
    housing_id = Column(Integer, ForeignKey('housings.housing_id'), nullable=False)
    time = Column(Date, nullable=False)
    grade = Column(Integer, nullable=False)

    tenant = relationship("Tenant", back_populates="reviews")
    housing = relationship("Housing", back_populates="reviews")

class Housing(Base):
    __tablename__ = 'housings'

    housing_id = Column(Integer, primary_key=True, autoincrement=True)
    address_id = Column(Integer, ForeignKey('addresses.address_id'), unique=True, nullable=False)
    ranting_id = Column(Integer, ForeignKey('renting_persons.ranting_id'), nullable=False)
    cost = Column(Integer, nullable=False)
    maximum_number_of_guests = Column(Integer, nullable=False)
    number_of_rooms = Column(Integer, nullable=False)
    area = Column(Integer, nullable=False)
    Type = Column(String(50), nullable=False)

    address = relationship("Address", uselist=False, back_populates="housing")
    renting_person = relationship("RentingPerson", back_populates="housings")
    bookings = relationship("Booking", back_populates="housing")
    reviews = relationship("Review", back_populates="housing")

class Address(Base):
    __tablename__ = 'addresses'

    address_id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String(100), nullable=False)
    city = Column(String(50), nullable=False)
    road = Column(String(100), nullable=False)
    house = Column(String(10), nullable=False)

    housing = relationship("Housing", uselist=False, back_populates="address")