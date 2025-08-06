from fastapi import FastAPI
from db import Base, engine
from routes import prediction, index_tests
from utils.data_spammer import spam_deliveries
#https://www.kaggle.com/datasets/willianoliveiragibin/food-delivery-time?resource=download
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Register routes
app.include_router(prediction.router)
app.include_router(index_tests.router)

@app.post("/spam")
def run_spammer():
    spam_deliveries(10000)
    return {"message": "Database filled with fake deliveries"}