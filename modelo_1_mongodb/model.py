import uuid
from typing import Optional
from pydantic import BaseModel, Field

    
class Airline(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "name": "Delta"
            }
        }

class City(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "name": "New York"
            }
        }

class Flight_Search(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    airline_id: str = Field(...)
    from_city_id: str = Field(...)
    to_city_id: str = Field(...)
    day: int = Field(...)
    month: int = Field(...)
    year: int = Field(...)
    duration: int = Field(...)
    age: int = Field(...)
    gender: str = Field(...)
    reason: str = Field(...)
    stay: str = Field(...)
    transit: str = Field(...)
    connection: bool = Field(...)
    wait: int = Field(...)
    ticket: str = Field(...)
    checked_bags: int = Field(...)
    carry_on: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "airline_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "from_city_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "to_city_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "day": 1,
                "month": 1,
                "year": 2020,
                "duration": 120,
                "age": 25,
                "gender": "male",
                "reason": "business",
                "stay": "hotel",
                "transit": "yes",
                "connection": True,
                "wait": 60,
                "ticket": "economy",
                "checked_bags": 2,
                "carry_on": "yes"
            }
        }

class Flight_Insert(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    airline: str = Field(...)
    from_city: str = Field(...)
    to: str = Field(...)
    day: int = Field(...)
    month: int = Field(...)
    year: int = Field(...)
    duration: int = Field(...)
    age: int = Field(...)
    gender: str = Field(...)
    reason: str = Field(...)
    stay: str = Field(...)
    transit: str = Field(...)
    connection: bool = Field(...)
    wait: int = Field(...)
    ticket: str = Field(...)
    checked_bags: int = Field(...)
    carry_on: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "airline": "Delta Airlines",
                "from_city": "GDL",
                "to": "PDX",
                "day": 1,
                "month": 1,
                "year": 2020,
                "duration": 120,
                "age": 25,
                "gender": "male",
                "reason": "business",
                "stay": "hotel",
                "transit": "yes",
                "connection": True,
                "wait": 60,
                "ticket": "economy",
                "checked_bags": 2,
                "carry_on": "yes"
            }
        }

class Flight_Common_Destinations(BaseModel):
    id: dict = Field(alias="_id")
    count: int = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": {
                    "from_city": "GDL",
                    "to_city": "PDX"
                },
                "count": 10
            }
        }

class Flight_Average_Duration(BaseModel):
    id: dict = Field(alias="_id")
    avg_duration: float = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": {
                    "from_city": "GDL",
                    "to_city": "PDX"
                },
                "avg_duration": 120.0
            }
        }

class Flight_Popular_Airlines(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    count: int = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "Aeromexico",
                "count": 10
            }
        }
