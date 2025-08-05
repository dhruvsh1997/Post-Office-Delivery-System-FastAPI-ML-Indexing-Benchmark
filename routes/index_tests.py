from fastapi import APIRouter
from sqlalchemy.orm import Session
from db import SessionLocal
from models import Delivery
import time

router = APIRouter()

@router.get("/deliveries/traffic-level/no-index")
def get_deliveries_no_index(level: str):
    db: Session = SessionLocal()
    start = time.time()
    deliveries = db.query(Delivery).filter(Delivery.traffic_level == level).all()
    duration = time.time() - start
    db.close()
    return {"count": len(deliveries), "time_taken_sec": round(duration, 4)}

@router.get("/deliveries/traffic-level/with-index")
def get_deliveries_with_index(level: str):
    db: Session = SessionLocal()

    # NOTE: You must manually create index via SQL for this test
    # e.g., CREATE INDEX idx_traffic_level ON deliveries(traffic_level);

    start = time.time()
    deliveries = db.query(Delivery).filter(Delivery.traffic_level == level).all()
    duration = time.time() - start
    db.close()
    return {"count": len(deliveries), "time_taken_sec": round(duration, 4)}