import csv
import requests

BASE_URL = "http://localhost:8000"

def arlines():
    with open("flight_passengers.csv") as fd:
        flight_passenger_csv = csv.DictReader(fd)
        # create a set of airlines to avoid duplicates in the database
        airlines = set()

        # get all airlines
        for flight in flight_passenger_csv:
            airlines.add(flight["airline"])

        # for each airline, post it to the API
        for airline in airlines:
            x = requests.post(BASE_URL+"/airline", json={"name": airline})
            if not x.ok:
                print(f"Failed to post airline {x} - {airline}")


def cities():
    with open("flight_passengers.csv") as fd:
        flight_passenger_csv = csv.DictReader(fd)
        # create a set of cities to avoid duplicates in the database
        cities = set()

        # get all cities
        for flight in flight_passenger_csv:
            cities.add(flight["from"])
            cities.add(flight["to"])
        
        # for each city, post it to the API
        for city in cities:
            x = requests.post(BASE_URL+"/city", json={"name": city})
            if not x.ok:
                print(f"Failed to post city {x} - {city}")


def flights():
    with open("flight_passengers.csv") as fd:
        flight_passenger_csv = csv.DictReader(fd)
        for flight in flight_passenger_csv:
            # change from property to from_city
            flight["from_city"] = flight.pop("from")

            x = requests.post(BASE_URL+"/flight", json=flight)
            if not x.ok:
                print(f"Failed to post flight {x} - {flight}")

def main():
    arlines()
    cities()
    flights()


if __name__ == "__main__":
    main()
