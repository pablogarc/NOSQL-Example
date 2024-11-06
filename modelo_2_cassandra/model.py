#!/usr/bin/env python3
import logging
from datetime import datetime

# Set logger
log = logging.getLogger()

# tabless -----
CREATE_KEYSPACE = """
        CREATE KEYSPACE IF NOT EXISTS {}
        WITH replication = {{ 'class': 'SimpleStrategy', 'replication_factor': {} }}
"""

CREATE_FLIGHTS_TABLE = """
    CREATE TABLE IF NOT EXISTS flights (
        flight_id TEXT,
        airline TEXT,
        from_city TEXT,
        to_city TEXT,
        day INT,
        month INT,
        year INT,
        connection BOOLEAN,
        PRIMARY KEY ((from_city, to_city, year), flight_id)
    ) WITH CLUSTERING ORDER BY (flight_id ASC);
"""

CREATE_TABLE_FLIGHTS_FROM = """
    CREATE TABLE IF NOT EXISTS flights_from (
        from_city TEXT,
        month INT,
        year INT,
        flight_id TEXT,
        airline TEXT,
        to_city TEXT,
        day INT,
        connection BOOLEAN,
        PRIMARY KEY ((from_city, year), flight_id)
) WITH CLUSTERING ORDER BY (flight_id ASC);
"""

CREATE_TABLE_FLIGHTS_TO = """
    CREATE TABLE IF NOT EXISTS flights_to (
        to_city TEXT,
        month INT,
        year INT,
        flight_id TEXT,
        airline TEXT,
        from_city TEXT,
        day INT,
        connection BOOLEAN,
        PRIMARY KEY ((to_city, year), flight_id)
) WITH CLUSTERING ORDER BY (flight_id ASC);
"""

CREATE_TICKETS_BY_FLIGHT_TABLE = """
    CREATE TABLE IF NOT EXISTS tickets_by_f_t (
        ticket_id TEXT,
        flight_id TEXT,
        ticket TEXT,
        checked_bags INT,
        carry_on BOOLEAN,
        month INT,
        year INT,
        day INT,
         PRIMARY KEY ((ticket), checked_bags, ticket_id, flight_id)
    ) WITH CLUSTERING ORDER BY (checked_bags DESC, ticket_id ASC, flight_id ASC);
"""


# Queryssss----
SELECT_ALL_FLIGHTS = """
    SELECT *
    FROM flights
"""

SELECT_FLIGHT_BY_ID = """
    SELECT *
    FROM flights
    WHERE flight_id = ?
"""

SELECT_FLIGHTS_BY_CONNECTION = """
    SELECT connection
    FROM flights
    WHERE flight_id = ?
    ALLOW FILTERING
"""

SELECT_TICKETS_BY_TYPE = """
    SELECT ticket
    FROM tickets_by_f_t
    WHERE ticket_id = ?
"""

SELECT_FLIGHTS_IDS = """
    SELECT flight_id
    FROM flights
"""

SELECT_TICKETS_IDS = """
    SELECT ticket_id
    FROM tickets_by_f_t
"""

COUNT_FROM_FLIGHTS_FROM_FLIGHTS = """
    SELECT COUNT(*)
    FROM flights_from
    WHERE from_city = ?
    AND year = ?
"""

COUNT_FROM_FLIGHTS_TO_FLIGHTS = """
    SELECT COUNT(*)
    FROM flights_to
    WHERE to_city = ?
    AND year = ?
"""

QUERY_LUGGAGE_SPECIFIC = """
    SELECT ticket_id, flight_id, checked_bags 
    FROM tickets_by_f_t
    WHERE ticket = ? 
    AND checked_bags > ?;
"""

QUERY_LUGGAGE_UP_TO_TWO = """
    SELECT ticket_id, flight_id, checked_bags 
    FROM tickets_by_f_t
    WHERE ticket = ? 
    AND checked_bags > 2;
"""
#Car rent
def create_keyspace(session, keyspace, replication_factor):
    log.info(f"Creating keyspace: {keyspace} with replication factor {replication_factor}")
    session.execute(CREATE_KEYSPACE.format(keyspace, replication_factor))


def create_schema(session):
    log.info("Creating model schema")
    session.execute(CREATE_FLIGHTS_TABLE)
    session.execute(CREATE_TICKETS_BY_FLIGHT_TABLE)
    session.execute(CREATE_TABLE_FLIGHTS_FROM)
    session.execute(CREATE_TABLE_FLIGHTS_TO)


def get_all_flights(session):
    log.info("Retrieving all flights")
    stmt = session.prepare(SELECT_ALL_FLIGHTS)
    rows = session.execute(stmt)
    for row in rows:
        print(f"=== Flight: {row.flight_id} ===")
        print(f"- Airline: {row.airline}")
        print(f"- From: {row.from_city}")
        print(f"- To: {row.to_city}")
        print(f"- Date: {row.day}/{row.month}/{row.year}")
        print(f"- Connection: {row.connection}")


def get_flight_by_id(session, flight_id):
    log.info(f"Retrieving flight {flight_id}")
    stmt = session.prepare(SELECT_FLIGHT_BY_ID)
    rows = session.execute(stmt, [flight_id])
    for row in rows:
        print(f"=== Flight: {row.flight_id} ===")
        print(f"- Airline: {row.airline}")
        print(f"- From: {row.from_city}")
        print(f"- To: {row.to_city}")
        print(f"- Date: {row.day}/{row.month}/{row.year}")
        print(f"- Connection: {row.connection}")


def get_flights_by_connection(session):
    log.info("Retrieving flights by connection type")
    stmt = session.prepare(SELECT_FLIGHTS_BY_CONNECTION)
    query = session.execute(SELECT_FLIGHTS_IDS)

    flight_ids = []
    count_true = 0
    count_false = 0

    for row in query:
        flight_ids.append(row.flight_id)

    for flight_id in flight_ids:
        rows = session.execute(stmt, [flight_id])
        for row in rows:
            if row.connection:
                count_true += 1
            else:
                count_false += 1
        
    print(f"=== Connection: True ===")
    print(f"Total: {count_true}")
    print(f"=== Connection: False ===")
    print(f"Total: {count_false}")


def get_tickets_by_type(session):
    log.info("Retrieving tickets by type")
    stmt = session.prepare(SELECT_TICKETS_BY_TYPE)
    query = session.execute(SELECT_TICKETS_IDS)

    ticket_ids = []
    economy = 0
    business = 0
    first_class = 0

    for row in query:
        ticket_ids.append(row.ticket_id)
    
    for ticket_id in ticket_ids:
        rows = session.execute(stmt, [ticket_id])
        for row in rows:
            if row.ticket == "Economy":
                economy += 1
            elif row.ticket == "Business":
                business += 1
            elif row.ticket == "First Class":
                first_class += 1
    
    print(f"=== Ticket Type: Economy ===")
    print(f"Total: {economy}")
    print(f"=== Ticket Type: Business ===")
    print(f"Total: {business}")
    print(f"=== Ticket Type: First Class ===")
    print(f"Total: {first_class}")
        

# Función para obtener el tráfico total de cada aeropuerto por mes y año
#total
def get_total_traffic_by_airport(session, airport_code, year):
    # Recupera el número de salidas del aeropuerto
    departures = get_departures_by_airport(session, airport_code, year)
    # Recupera el número de llegadas al aeropuerto
    arrivals = get_arrivals_by_airport(session, airport_code, year)

    # Suma ambos valores para obtener el tráfico total
    total_traffic = departures + arrivals

    if total_traffic > 0:
        print("=============================================================")
        print(f"Total traffic for the {airport_code} in {year}: {total_traffic}\n\n")
    else:
        print("-----------------------------------------------------")
        print("no data")

    log.info(f"Total traffic at {airport_code} during {year}: {total_traffic}")
    return total_traffic

#from
def get_departures_by_airport(session, airport_code, year):
    log.info(f"Retrieving departures from {airport_code} in {year}")

    stmt = session.prepare(COUNT_FROM_FLIGHTS_FROM_FLIGHTS)
    result = session.execute(stmt, [airport_code, year]).one()


    if result[0] > 0:
        print("\n=============================================================")
        print(f"Total departures from {airport_code} in {year}: {result[0]}")
    else:
        print(f"No data available for {airport_code} in {year}")
    
    return result[0]

#to
def get_arrivals_by_airport(session, airport_code, year):
    log.info(f"Retrieving arrivals to {airport_code} in {year}")

    stmt = session.prepare(COUNT_FROM_FLIGHTS_TO_FLIGHTS)
    result = session.execute(stmt, [airport_code, year]).one()

    if result[0] > 0:
        print("\n=============================================================")
        print(f"Total arrivals to {airport_code} in {year}: {result[0]}")
    else:
        print(f"No data available for {airport_code} in {year}")

    return result[0]


def get_high_end_tickets_with_extra_luggage(session, ticket_type):
    log.info("Retrieving tickets for ticket type with more than 2 checked bags")

    stmt = session.prepare(QUERY_LUGGAGE_UP_TO_TWO)
    result = session.execute(stmt, [ticket_type])

    print("===============================================================")
    for row in result:
        print(f"Ticket ID: {row.ticket_id}, Flight ID: {row.flight_id}")

    print()


def get_high_end_tickets_with_given_luggage(session, ticket_type, luggage_qty):
    log.info("Retrieving tickets for ticket type with a given qty of checked bags")

    stmt = session.prepare(QUERY_LUGGAGE_SPECIFIC)
    result = session.execute(stmt, [ticket_type, luggage_qty])

    print("===============================================================")
    for row in result:
        print(f"Ticket ID: {row.ticket_id}, Flight ID: {row.flight_id}")

    print()