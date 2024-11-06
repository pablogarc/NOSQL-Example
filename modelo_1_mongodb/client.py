import argparse
import logging
import os
import requests
import asyncio


# Set logger
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('flights.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Read env vars related to API connection
FLIGHTS_API_URL = os.getenv("FLIGHTS_API_URL", "http://localhost:8000")


def print_flight(flight):
    for k in flight.keys():
        print(f"{k}: {flight[k]}")
    print("="*50)

def print_airline(airline):
    for k in airline.keys():
        print(f"{k}: {airline[k]}")
    print("="*50)

def print_city(city):
    for k in city.keys():
        print(f"{k}: {city[k]}")
    print("="*50)


def list_flights(limit, skip):
    suffix = "/flight"
    endpoint = FLIGHTS_API_URL + suffix
    params = {
        "limit": limit,
        "skip": skip
    }
    response = requests.get(endpoint, params=params)
    if response.ok:
        json_resp = response.json()
        for flight in json_resp:
            print_flight(flight)
    else:
        print(f"Error: {response}")

def get_flight_by_id(id):
    suffix = f"/flight/{id}"
    endpoint = FLIGHTS_API_URL + suffix
    response = requests.get(endpoint)
    if response.ok:
        json_resp = response.json()
        print_flight(json_resp)
    else:
        print(f"Error: {response}")


def list_airlines(limit, skip):
    suffix = "/airline"
    endpoint = FLIGHTS_API_URL + suffix
    params = {
        "limit": limit,
        "skip": skip
    }
    response = requests.get(endpoint, params=params)
    if response.ok:
        json_resp = response.json()
        for airline in json_resp:
            print_airline(airline)
    else:
        print(f"Error: {response}")

def get_airline_by_id(id):
    suffix = f"/airline/{id}"
    endpoint = FLIGHTS_API_URL + suffix
    response = requests.get(endpoint)
    if response.ok:
        json_resp = response.json()
        print_airline(json_resp)
    else:
        print(f"Error: {response}")


def list_cities(limit, skip):
    suffix = "/city"
    endpoint = FLIGHTS_API_URL + suffix
    params = {
        "limit": limit,
        "skip": skip
    }
    response = requests.get(endpoint, params=params)
    if response.ok:
        json_resp = response.json()
        for city in json_resp:
            print_city(city)
    else:
        print(f"Error: {response}")

def get_city_by_id(id):
    suffix = f"/city/{id}"
    endpoint = FLIGHTS_API_URL + suffix
    response = requests.get(endpoint)
    if response.ok:
        json_resp = response.json()
        print_city(json_resp)
    else:
        print(f"Error: {response}")


def common_destinations(limit, skip):
    suffix = "/flight/common_destinations/"
    endpoint = FLIGHTS_API_URL + suffix
    params = {
        "limit": limit,
        "skip": skip
    }
    response = requests.get(endpoint, params=params)
    if response.ok:
        json_resp = response.json()
        for flight in json_resp:
            print_flight(flight)
    else:
        print(f"Error: {response}")


def average_duration(limit, skip):
    suffix = "/flight/average_duration/"
    endpoint = FLIGHTS_API_URL + suffix
    params = {
        "limit": limit,
        "skip": skip
    }
    response = requests.get(endpoint, params=params)
    if response.ok:
        json_resp = response.json()
        for flight in json_resp:
            print_flight(flight)
    else:
        print(f"Error: {response}")


def popular_airlines(limit, skip):
    suffix = "/flight/popular_airlines/"
    endpoint = FLIGHTS_API_URL + suffix
    params = {
        "limit": limit,
        "skip": skip
    }
    response = requests.get(endpoint, params=params)
    if response.ok:
        json_resp = response.json()
        for flight in json_resp:
            print_flight(flight)
    else:
        print(f"Error: {response}")


def main():
    log.info(f"Welcome to flights catalog. App requests to: {FLIGHTS_API_URL}")

    parser = argparse.ArgumentParser()

    list_of_actions = ["search_flights", "get_flight", "search_airlines", "get_airline", "search_cities", "get_city", "common_destinations", "average_duration", "popular_airlines"]
    parser.add_argument("action", choices=list_of_actions,
            help="Action to be user for the flight catalog")
    parser.add_argument("-i", "--id",
            help="Provide a flight ID, city ID or airline ID which related to the flight catalog action", default=None)
    parser.add_argument("-l", "--limit",
            help="Limit the number of flights, cities or airlines to be shown", default=None)
    parser.add_argument("-s", "--skip",
            help="Skip the first N flights, cities or airlines", default=None) 

    args = parser.parse_args()

    if args.id and not args.action in ["get_flight", "get_airline", "get_city"]:
        log.error(f"Can't use arg id with action {args.action}")
        exit(1)

    if (args.limit or args.skip) and not args.action in ["search_flights", "search_airlines", "search_cities", "common_destinations", "average_duration", "popular_airlines"]:
        log.error(f"Limit, and skip arg can only be used with search action")
        exit(1)

    if args.action == "search_flights": # get list of flights
        list_flights(args.limit, args.skip)
    elif args.action == "get_flight": # get flight by id
        get_flight_by_id(args.id)

    elif args.action == "search_airlines": # get id of airlines
        list_airlines(args.limit, args.skip)
    elif args.action == "get_airline": # get stats for airline by id (impotant for my solution)
        get_airline_by_id(args.id)

    elif args.action == "search_cities": # get list of cities
        list_cities(args.limit, args.skip)
    elif args.action == "get_city": # get stats for city by id (important for my solution)
        get_city_by_id(args.id)

    elif args.action == "common_destinations": # get common destinations (extra feature)
        common_destinations(args.limit, args.skip)

    elif args.action == "average_duration": # get average duration of flights (extra feature)
        average_duration(args.limit, args.skip)

    elif args.action == "popular_airlines": # get popular airlines (extra feature)
        popular_airlines(args.limit, args.skip)

if __name__ == "__main__":
    main()
