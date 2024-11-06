from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from model import City

router = APIRouter()

@router.post("/", response_description="Post a new city", status_code=status.HTTP_201_CREATED, response_model=City)
def create_city(request: Request, city: City = Body(...)):
    city = jsonable_encoder(city)
    new_city = request.app.database["cities"].insert_one(city)
    created_city = request.app.database["cities"].find_one(
        {"_id": new_city.inserted_id}
    )

    return created_city


@router.get("/", response_description="Get all cities", response_model=List[City])
def list_cities(request: Request, limit: int = 20, skip: int = 0):
    cities = list(request.app.database["cities"].find().skip(skip).limit(limit))
    return cities


@router.get("/{id}", response_description="Get stats for a single city by id")
def find_city(id: str, request: Request):
    city = request.app.database["cities"].find_one({"_id": id })
    flights = list(request.app.database["flights"].find({"from_city_id": id}))

    # calculate the number of flights for that city
    num_flights = len(flights)

    # get the most popular to_city_id for the city id we received as a parameter where the city is the from_city_id
    most_popular_destination = max(
        [(flight["to_city_id"]) for flight in flights],
        key=lambda x: (x)
    )

    # get the destination city name from the city id (from_city, to_city)
    to_city = request.app.database["cities"].find_one({"_id": most_popular_destination})

    # calculate the best month to travel from that city
    months = {}
    for flight in flights:
        if flight["month"] in months:
            months[flight["month"]] += 1
        else:
            months[flight["month"]] = 1
    best_month = max(months, key=months.get)

    # convert the month number to month name
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    best_month = months[best_month - 1]

    # calculate the average duration of the flights from that city
    durations = [flight["duration"] for flight in flights]
    avg_duration = sum(durations) / len(durations)

    # what airline has the most flights from/to that city
    airlines = {}
    for flight in flights:
        if flight["airline_id"] in airlines:
            airlines[flight["airline_id"]] += 1
        else:
            airlines[flight["airline_id"]] = 1
    most_flights_airline = max(airlines, key=airlines.get)

    # get the airline name from the airline id
    airline = request.app.database["airlines"].find_one({"_id": most_flights_airline})

    return {
        "city": city["name"],
        f"num_flights from {city['name']}": num_flights,
        f"most_popular_destination (to_city) for {city['name']}": to_city["name"],
        f"best_month to travel from {city['name']}": best_month,
        f"avg_duration from {city['name']}": avg_duration,
        f"most_flights_airline from {city['name']}": airline["name"]
    }
