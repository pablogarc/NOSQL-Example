from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from model import Airline

router = APIRouter()

@router.post("/", response_description="Post a new airline", status_code=status.HTTP_201_CREATED, response_model=Airline)
def create_airline(request: Request, airline: Airline = Body(...)):
    airline = jsonable_encoder(airline)
    new_airline = request.app.database["airlines"].insert_one(airline)
    created_airline = request.app.database["airlines"].find_one(
        {"_id": new_airline.inserted_id}
    )

    return created_airline


@router.get("/", response_description="Get all airlines", response_model=List[Airline])
def list_airlines(request: Request, limit: int = 20, skip: int = 0):
    airlines = list(request.app.database["airlines"].find().skip(skip).limit(limit))
    return airlines


@router.get("/{id}", response_description="Get stats for a single airline by id")
def airline_stats(id: str, request: Request):
    airline = request.app.database["airlines"].find_one({"_id": id})
    flights = list(request.app.database["flights"].find({"airline_id": id}))

    # calculate the number of flights for that airline
    num_flights = len(flights)

    # get the most popular destination (from_city_id, to_city_id) for that airline
    most_popular_destination = max(
        [(flight["from_city_id"], flight["to_city_id"]) for flight in flights],
        key=lambda x: (x[0], x[1])
    )
  
    # get the destination city name from the city id (from_city, to_city)
    from_city = request.app.database["cities"].find_one({"_id": most_popular_destination[0]})
    to_city = request.app.database["cities"].find_one({"_id": most_popular_destination[1]})

    # calculate the best month to travel in that airline
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

    # calculate the average age of the passengers for that airline
    ages = [passenger["age"] for passenger in flights]
    avg_age = sum(ages) / len(ages)

    # calculate the number of passengers for most popular destination for that airline
    passengers = [flight["age"] for flight in flights if flight["from_city_id"] == most_popular_destination[0] and flight["to_city_id"] == most_popular_destination[1]]

    return {
        "airline": airline["name"],
        f"num_flights in {airline['name']}": num_flights,
        "most_popular_destination": f"{from_city['name']} to {to_city['name']}",
        f"best_month to travel in {airline['name']}": best_month,
        f"avg_age of passengers in {airline['name']}": avg_age,
        f"passengers_for_most_popular_destination in {airline['name']}": len(passengers)
    }