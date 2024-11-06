#!/usr/bin/env python3
import logging
import os
import random

from cassandra.cluster import Cluster

import model

# Set logger
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('flights.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Read env vars releated to Cassandra App
CLUSTER_IPS = os.getenv('CASSANDRA_CLUSTER_IPS', 'localhost')
KEYSPACE = os.getenv('CASSANDRA_KEYSPACE', 'flights')
REPLICATION_FACTOR = os.getenv('CASSANDRA_REPLICATION_FACTOR', '1')


def print_menu():
    mm_options = {
        1: "Show all flights",
        2: "Show flight by ID",
        3: "Show total flights by connection type",
        4: "Show total tickets by type",
        5: "Show total traffic by airport for a specific year",
        6: "Show arrivals by airport for a specific year",
        7: "Show departures by airport for a specific year",
        8: "Show flights with a ticket type with extra luggage (luggage > 2)",
        9: "Show flights with a ticket type with extra luggage (luggage > n)",
        10: "Exit"
    }
    for key, value in mm_options.items():
        print(f"{key} -- {value}")

def main():
    log.info("Connecting to Cluster")
    cluster = Cluster(CLUSTER_IPS.split(','))
    session = cluster.connect()

    model.create_keyspace(session, KEYSPACE, int(REPLICATION_FACTOR))
    session.set_keyspace(KEYSPACE)
    
    model.create_schema(session)

    while True:
        print_menu()
        option = int(input('Enter your choice: '))
        if option == 1:
            model.get_all_flights(session)
        elif option == 2:
            flight_id = input('Enter flight ID: ')
            model.get_flight_by_id(session, flight_id)
        elif option == 3:
            model.get_flights_by_connection(session)
        elif option == 4:
            model.get_tickets_by_type(session)
        elif option == 5:
            airport_code = input('Enter airport code: ')
            year = int(input('Enter year: '))
            model.get_total_traffic_by_airport(session, airport_code, year)
        elif option == 6:
            airport_code = input('Enter airport code: ')
            year = int(input('Enter year: '))
            model.get_arrivals_by_airport(session, airport_code, year)
        elif option == 7:
            airport_code = input('Enter airport code: ')
            year = int(input('Enter year: '))
            model.get_departures_by_airport(session, airport_code, year)
        elif option == 8:
            ticket_type = input('Enter ticket type: ')
            model.get_high_end_tickets_with_extra_luggage(session, ticket_type)
        elif option == 9:
            ticket_type = input('Enter ticket type: ')
            n = int(input('Enter a quantity to search (lugage > quantity): '))
            model.get_high_end_tickets_with_given_luggage(session, ticket_type, n)
        elif option == 10:
            log.info("Exiting program")
            break


if __name__ == '__main__':
    main()