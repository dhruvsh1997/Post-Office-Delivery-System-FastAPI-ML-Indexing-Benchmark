from models import Delivery, DeliveryPerson, Package, PostOffice, Customer, Vehicle
from sqlalchemy.orm import Session
from db import SessionLocal
from faker import Faker
import random
import numpy as np

def spam_deliveries(n=1000):
    db = SessionLocal()
    fake = Faker()
    persons = db.query(DeliveryPerson).all()
    packages = db.query(Package).all()
    offices = db.query(PostOffice).all()

    for _ in range(n):
        delivery = Delivery(
            delivery_person_id=random.choice(persons).id,
            package_id=random.choice(packages).id,
            post_office_id=random.choice(offices).id,
            traffic_level=random.choice(["Low", "Medium", "High"]),
            weather_description=random.choice(['mist', 'clear sky', 'overcast clouds', 'broken clouds', 'haze','scattered clouds', 'fog', 'smoke', 'few clouds','light rain', 'moderate rain']),
            temperature=random.uniform(20, 40),
            humidity=random.uniform(30, 90),
            precipitation=random.uniform(0, 10),
            distance=random.uniform(1, 50),
            delivery_time=random.uniform(0.5, 10)
        )
        db.add(delivery)
    db.commit()
    db.close()

# utils/data_spammer.py
def seed_initial_data():
    db = SessionLocal()
    fake = Faker()

    # Create vehicles
    vehicle_types = ["Bike", "Scooter", "Car", "Van"]
    vehicles = []
    for vt in vehicle_types:
        v = Vehicle(type=vt)
        db.add(v)
        vehicles.append(v)
    db.commit()

    # Create post offices
    offices = []
    for _ in range(5):
        office = PostOffice(
            name=fake.company(),
            latitude=random.uniform(-90, 90),
            longitude=random.uniform(-180, 180)
        )
        db.add(office)
        offices.append(office)
    db.commit()

    # Create delivery persons
    for _ in range(10):
        dp = DeliveryPerson(
            name=fake.name(),
            age=random.randint(20, 50),
            rating=round(random.uniform(3, 5), 1),
            vehicle_id=random.choice(vehicles).id   
        )
        db.add(dp)
    db.commit()

    # Create customers and packages
    for _ in range(20):
        customer = Customer(
            name=fake.name(),
            latitude=random.uniform(-90, 90),
            longitude=random.uniform(-180, 180)
        )
        db.add(customer)
        db.commit()
        pkg = Package(
            type=random.choice(["Documents", "Electronics", "Clothing"]),
            weight=round(random.uniform(0.5, 10), 2),
            customer_id=customer.id
        )
        db.add(pkg)
    db.commit()

    db.close()
