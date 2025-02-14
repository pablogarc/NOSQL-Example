import os

from fastapi import FastAPI
from pymongo import MongoClient

from routes.airline_routes import router as airline_router
from routes.city_routes import router as city_router
from routes.flight_routes import router as flight_router


MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
DB_NAME = os.getenv('MONGODB_DB_NAME', 'flight_passenger')

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(MONGODB_URI)
    app.database = app.mongodb_client[DB_NAME]
    print(f"Connected to MongoDB at: {MONGODB_URI} \n\t Database: {DB_NAME}")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
    print("Bye bye...!!")

app.include_router(airline_router, tags=["airlines"], prefix="/airline")
app.include_router(city_router, tags=["cities"], prefix="/city")
app.include_router(flight_router, tags=["flights"], prefix="/flight")
