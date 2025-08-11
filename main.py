from fastapi import FastAPI
from db import Base, engine
from routes import prediction, index_tests
from utils.data_spammer import seed_initial_data, spam_deliveries
#https://www.kaggle.com/datasets/willianoliveiragibin/food-delivery-time?resource=download
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Register routes
app.include_router(prediction.router)
app.include_router(index_tests.router)

@app.post("/seed-and-spam")
def seed_and_spam():
    seed_initial_data()
    # breakpoint()
    spam_deliveries(1000)
    return {"message": "Database seeded and filled with fake deliveries"}