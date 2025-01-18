from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Tenant, RentingPerson, PaymentMethod, Booking, Review, Housing, Address
from faker import Faker
import random
from sqlalchemy.sql import text
from datetime import timedelta

DATABASE_URL = "postgresql://postgres:........@localhost/airbnb"
engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)
session = Session()

def populate_users(session, count=20000):
    fake = Faker()
    users = []
    emails = set()

    for _ in range(count):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = f"{first_name.lower()}.{last_name.lower()}@example.com"

        # Убеждаемся, что email уникален
        while email in emails:
            email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 1000)}@example.com"
        emails.add(email)

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            contact=fake.phone_number(),
            bio=fake.text(max_nb_chars=500),
            date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=50)
        )
        users.append(user)

    session.add_all(users)
    session.commit()

def populate_tenants(session, count=11000):
    users = session.query(User).all()
    random.shuffle(users)  # Перемешиваем пользователей для случайного выбора

    tenants = []
    for user in users[:count]:
        tenant = Tenant(user_id=user.user_id)
        tenants.append(tenant)

    session.add_all(tenants)
    session.commit()

def populate_renting_persons(session):
    users = session.query(User).all()
    tenants = session.query(Tenant).all()
    tenant_user_ids = {tenant.user_id for tenant in tenants}

    renting_persons = []
    for user in users:
        if user.user_id not in tenant_user_ids:
            renting_person = RentingPerson(user_id=user.user_id)
            renting_persons.append(renting_person)

    session.add_all(renting_persons)
    session.commit()

def populate_payment_methods(session):
    banks = [
        "Bank of America", "JPMorgan Chase", "Wells Fargo", "Citigroup", "Goldman Sachs",
        "Morgan Stanley", "U.S. Bancorp", "PNC Financial Services", "Truist Financial",
        "TD Bank", "Capital One", "HSBC Bank USA", "Barclays Bank", "Santander Bank",
        "Citizens Bank", "KeyBank", "Regions Bank", "BB&T", "SunTrust Bank", "Fifth Third Bank",
        "Comerica Bank", "Zions Bancorporation", "Huntington Bancshares", "M&T Bank",
        "BMO Harris Bank", "First Republic Bank", "Silicon Valley Bank", "Signature Bank",
        "Ally Financial", "Discover Financial", "Synchrony Financial", "American Express",
        "Charles Schwab Corporation", "E*TRADE Financial", "Vanguard Group", "Fidelity Investments",
        "State Street Corporation", "Northern Trust", "T. Rowe Price", "BlackRock", "Invesco",
        "Franklin Resources"
    ]

    fake = Faker()
    tenants = session.query(Tenant).all()

    payment_methods = []
    for tenant in tenants:
        used_banks = set()  # Множество для отслеживания использованных банков
        num_methods = random.randint(1, 3)  # Генерируем от 1 до 3 способов оплаты
        for _ in range(num_methods):
            bank = random.choice(banks)
            while bank in used_banks:
                bank = random.choice(banks)
            used_banks.add(bank)

            payment_method = PaymentMethod(
                ten_id=tenant.ten_id,
                pin=fake.random_number(digits=4, fix_len=True),
                number_of_card=fake.credit_card_number(),
                bank=bank
            )
            payment_methods.append(payment_method)

    session.add_all(payment_methods)
    session.commit()

def populate_addresses(session, count=27000):
    fake = Faker()
    real_cities = {
        "France": ["Paris", "Marseille", "Lyon", "Toulouse", "Nice"],
        "Spain": ["Madrid", "Barcelona", "Valencia", "Seville", "Zaragoza"],
        "United States": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"],
        "China": ["Beijing", "Shanghai", "Guangzhou", "Shenzhen", "Chengdu"],
        "Italy": ["Rome", "Milan", "Naples", "Turin", "Palermo"],
        "Turkey": ["Istanbul", "Ankara", "Izmir", "Bursa", "Antalya"],
        "Mexico": ["Mexico City", "Guadalajara", "Monterrey", "Puebla", "Tijuana"],
        "Germany": ["Berlin", "Hamburg", "Munich", "Cologne", "Frankfurt"],
        "Thailand": ["Bangkok", "Nonthaburi", "Nakhon Ratchasima", "Chiang Mai", "Hat Yai"],
        "United Kingdom": ["London", "Birmingham", "Glasgow", "Liverpool", "Bristol"],
        "Japan": ["Tokyo", "Yokohama", "Osaka", "Nagoya", "Sapporo"],
        "Australia": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"],
        "Austria": ["Vienna", "Graz", "Linz", "Salzburg", "Innsbruck"],
        "Greece": ["Athens", "Thessaloniki", "Patras", "Heraklion", "Larissa"],
        "Canada": ["Toronto", "Montreal", "Vancouver", "Calgary", "Ottawa"],
        "Russia": ["Moscow", "Saint Petersburg", "Novosibirsk", "Yekaterinburg", "Nizhny Novgorod"],
        "Portugal": ["Lisbon", "Porto", "Braga", "Setúbal", "Coimbra"],
        "Netherlands": ["Amsterdam", "Rotterdam", "The Hague", "Utrecht", "Eindhoven"],
        "South Korea": ["Seoul", "Busan", "Incheon", "Daegu", "Daejeon"],
        "Switzerland": ["Zurich", "Geneva", "Basel", "Lausanne", "Bern"],
        "Malaysia": ["Kuala Lumpur", "George Town", "Ipoh", "Shah Alam", "Johor Bahru"],
        "Indonesia": ["Jakarta", "Surabaya", "Bandung", "Medan", "Semarang"],
        "India": ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Ahmedabad"],
        "Vietnam": ["Ho Chi Minh City", "Hanoi", "Da Nang", "Hai Phong", "Can Tho"],
        "Brazil": ["São Paulo", "Rio de Janeiro", "Brasília", "Salvador", "Fortaleza"],
        "Egypt": ["Cairo", "Alexandria", "Giza", "Shubra El-Kheima", "Port Said"],
        "South Africa": ["Johannesburg", "Cape Town", "Durban", "Pretoria", "Port Elizabeth"],
        "Morocco": ["Casablanca", "Rabat", "Fes", "Marrakech", "Tangier"],
        "Saudi Arabia": ["Riyadh", "Jeddah", "Mecca", "Medina", "Dammam"],
        "United Arab Emirates": ["Dubai", "Abu Dhabi", "Sharjah", "Al Ain", "Ajman"]
    }

    unique_addresses = set()
    addresses = []

    while len(addresses) < count:
        country = random.choice(list(real_cities.keys()))
        city = random.choice(real_cities[country])
        road = fake.street_name()
        house = random.randint(1, 100)

        address = (country, city, road, house)
        if address not in unique_addresses:
            unique_addresses.add(address)
            addresses.append(Address(
                country=country,
                city=city,
                road=road,
                house=house
            ))

    session.add_all(addresses)
    session.commit()

def populate_housings(session):
    fake = Faker()
    renting_persons = session.query(RentingPerson).all()
    addresses = session.query(Address).all()

    # Перемешиваем адреса для случайного выбора
    random.shuffle(addresses)

    housings = []
    address_index = 0
    for renting_person in renting_persons:
        num_housings = random.randint(1, 3)  # Генерируем от 1 до 3 жилья
        for _ in range(num_housings):
            if address_index >= len(addresses):
                break  # Предотвращаем выход за пределы списка адресов
            address = addresses[address_index]
            address_index += 1

            number_of_rooms = random.randint(1, 5)
            if number_of_rooms == 1:
                cost = random.randint(50, 100)
                maximum_number_of_guests = random.randint(1, 2)
                area = random.randint(10, 30)
                Type = 'Apartment'
            elif number_of_rooms == 2:
                cost = random.randint(100, 200)
                maximum_number_of_guests = random.randint(1, 4)
                area = random.randint(30, 70)
                Type = 'Apartment'
            elif number_of_rooms == 3:
                cost = random.randint(200, 300)
                maximum_number_of_guests = random.randint(1, 6)
                area = random.randint(70, 100)
                Type = random.choice(['Apartment', 'House'])
            elif number_of_rooms == 4:
                cost = random.randint(300, 400)
                maximum_number_of_guests = random.randint(1, 8)
                area = random.randint(100, 150)
                Type = random.choice(['Apartment', 'House', 'Villa'])
            elif number_of_rooms == 5:
                cost = random.randint(400, 500)
                maximum_number_of_guests = random.randint(1, 10)
                area = random.randint(150, 200)
                Type = random.choice(['Apartment', 'House', 'Villa'])

            housing = Housing(
                address_id=address.address_id,
                ranting_id=renting_person.ranting_id,
                cost=cost,
                maximum_number_of_guests=maximum_number_of_guests,
                number_of_rooms=number_of_rooms,
                area=area,
                Type=Type
            )
            housings.append(housing)

    session.add_all(housings)
    session.commit()

def delete_unused_addresses(session):
    session.execute(text('DELETE FROM addresses WHERE address_id NOT IN (SELECT DISTINCT address_id FROM housings)'))
    session.commit()

def populate_bookings(session):
    fake = Faker()
    tenants = session.query(Tenant).all()
    housings = session.query(Housing).all()

    bookings = []
    for tenant in tenants:
        num_bookings = random.randint(0, 3)  # Генерируем от 0 до 3 броней для каждого арендующего
        for _ in range(num_bookings):
            housing = random.choice(housings)
            check_in_date = fake.date_between(start_date='-30d', end_date='+30d')
            departure_date = check_in_date + timedelta(days=random.randint(5, 14))
            number_of_guests = random.randint(1, housing.maximum_number_of_guests)
            booking = Booking(
                ten_id=tenant.ten_id,
                housing_id=housing.housing_id,
                departure_date=departure_date,
                number_of_guests=number_of_guests,
                check_in_date=check_in_date
            )
            bookings.append(booking)

    session.add_all(bookings)
    session.commit()

def populate_reviews(session):
    fake = Faker()
    tenants = session.query(Tenant).all()
    bookings = session.query(Booking).all()

    reviews = []
    for tenant in tenants:
        tenant_bookings = [booking for booking in bookings if booking.ten_id == tenant.ten_id]
        num_reviews = random.randint(0, 3)  # Генерируем от 0 до 3 отзывов для каждого арендующего
        reviewed_housings = set()  # Множество для отслеживания уже оставленных отзывов на каждое жилье
        for _ in range(num_reviews):
            if not tenant_bookings:
                break  # Предотвращаем выход за пределы списка броней
            booking = random.choice(tenant_bookings)
            if booking.housing_id in reviewed_housings:
                continue  # Пропускаем, если уже оставляли отзыв на это жилье
            reviewed_housings.add(booking.housing_id)
            time = fake.date_between(start_date=booking.check_in_date, end_date='+30d')
            review = Review(
                ten_id=tenant.ten_id,
                housing_id=booking.housing_id,
                time=time,
                grade=random.randint(1, 5)
            )
            reviews.append(review)

    session.add_all(reviews)
    session.commit()

# Заполнение таблиц
populate_users(session)
populate_tenants(session)
populate_renting_persons(session)
populate_payment_methods(session)
populate_addresses(session)
populate_housings(session)
delete_unused_addresses(session)
populate_bookings(session)
populate_reviews(session)
