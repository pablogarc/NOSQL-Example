#!/usr/bin/env python3
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from model import Flight_Insert, Flight_Search, Flight_Common_Destinations, Flight_Average_Duration, Flight_Popular_Airlines

router = APIRouter()

@router.post("/", response_description="Post a new flight", status_code=status.HTTP_201_CREATED, response_model=Flight_Search)
def create_flight(request: Request, flight: Flight_Insert = Body(...)):
    flight = jsonable_encoder(flight)

    flight["airline_id"] = request.app.database["airlines"].find_one({"name": flight["airline"]})["_id"]
    flight["from_city_id"] = request.app.database["cities"].find_one({"name": flight["from_city"]})["_id"]
    flight["to_city_id"] = request.app.database["cities"].find_one({"name": flight["to"]})["_id"]

    # drop unused fields
    del flight["airline"]
    del flight["from_city"]
    del flight["to"]

    new_flight = request.app.database["flights"].insert_one(flight)
    created_flight = request.app.database["flights"].find_one(
        {"_id": new_flight.inserted_id}
    )

    return created_flight


@router.get("/", response_description="Get all flights", response_model=List[Flight_Search])
def list_flights(request: Request, limit: int = 20, skip: int = 0):
    flights = list(request.app.database["flights"].find().skip(skip).limit(limit))
    return flights


@router.get("/{id}", response_description="Get a single flight by id", response_model=Flight_Search)
def find_flight(id: str, request: Request):
    if (flight := request.app.database["flights"].find_one({"_id": id})) is not None:
        return flight
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Flight with ID {id} not found")


@router.get("/common_destinations/", response_description="Get common destinations", response_model=List[Flight_Common_Destinations])
def common_destinations(request: Request, limit: int = 5, skip: int = 0):
    pipeline = [
        {
            "$lookup": {
                "from": "cities",
                "localField": "from_city_id",
                "foreignField": "_id",
                "as": "from_city"
            }
        },
        {
            "$unwind": "$from_city"
        },
        {
            "$lookup": {
                "from": "cities",
                "localField": "to_city_id",
                "foreignField": "_id",
                "as": "to_city"
            }
        },
        {
            "$unwind": "$to_city"
        },
        {
            "$group": {
                "_id": {"from_city": "$from_city.name", "to_city": "$to_city.name"},
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {"count": -1}
        },
        {
            "$skip": skip
        },
        {
            "$limit": limit
        }
    ]
    flights = list(request.app.database["flights"].aggregate(pipeline))

    return flights


@router.get("/average_duration/", response_description="Get average duration", response_model=List[Flight_Average_Duration])
def average_duration(request: Request, limit: int = 10, skip: int = 0):
    pipeline = [
        {
            "$lookup": {
                "from": "cities",
                "localField": "from_city_id",
                "foreignField": "_id",
                "as": "from_city"
            }
        },
        {
            "$unwind": "$from_city"
        },
        {
            "$lookup": {
                "from": "cities",
                "localField": "to_city_id",
                "foreignField": "_id",
                "as": "to_city"
            }
        },
        {
            "$unwind": "$to_city"
        },
        {
            "$group": {
                "_id": {"from_city": "$from_city.name", "to_city": "$to_city.name"},
                "avg_duration": {"$avg": "$duration"}
            }
        },
        {
            "$sort": {"avg_duration": 1}
        },
        {
            "$skip": skip
        },
        {
            "$limit": limit
        }
    ]

    flights = list(request.app.database["flights"].aggregate(pipeline))

    return flights


@router.get("/popular_airlines/", response_description="Get popular airlines", response_model=List[Flight_Popular_Airlines])
def popular_airlines(request: Request, limit: int = 2, skip: int = 0):
    pipeline = [
        {
            "$lookup": {
                "from": "airlines",
                "localField": "airline_id",
                "foreignField": "_id",
                "as": "airline"
            }
        },
        {
            "$unwind": "$airline"
        },
        {
            "$group": {
                "_id": "$airline.name",
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {"count": -1}
        },
        {
            "$skip": skip
        },
        {
            "$limit": limit
        }
    ]

    flights = list(request.app.database["flights"].aggregate(pipeline))

    return flights
    
