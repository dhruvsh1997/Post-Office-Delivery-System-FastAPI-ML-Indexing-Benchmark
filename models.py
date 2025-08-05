from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db import Base
import datetime

class PostOffice(Base):
    __tablename__ = "post_offices"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)

class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)

class DeliveryPerson(Base):
    __tablename__ = "delivery_persons"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    rating = Column(Float)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    vehicle = relationship("Vehicle")

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)

class Package(Base):
    __tablename__ = "packages"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    weight = Column(Float)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    customer = relationship("Customer")

class Delivery(Base):
    __tablename__ = "deliveries"
    id = Column(Integer, primary_key=True, index=True)
    delivery_person_id = Column(Integer, ForeignKey("delivery_persons.id"))
    package_id = Column(Integer, ForeignKey("packages.id"))
    post_office_id = Column(Integer, ForeignKey("post_offices.id"))
    traffic_level = Column(String, index=False)  # We'll create index later
    weather_description = Column(String)
    temperature = Column(Float)
    humidity = Column(Float)
    precipitation = Column(Float)
    distance = Column(Float)
    delivery_time = Column(Float)
    delivered_at = Column(DateTime, default=datetime.datetime.utcnow)

class PredictionLog(Base):
    __tablename__ = "prediction_logs"
    id = Column(Integer, primary_key=True, index=True)
    features_json = Column(String)
    predicted_time = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
