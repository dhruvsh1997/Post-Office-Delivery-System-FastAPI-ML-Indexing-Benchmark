from models import Delivery, DeliveryPerson, Package, PostOffice
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