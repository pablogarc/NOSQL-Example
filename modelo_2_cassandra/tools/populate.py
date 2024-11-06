#!/usr/bin/env python3
import datetime
import random
import uuid

CQL_FILE = 'data.cql'

airlines = ["American Airlines", "Delta Airlines", "Alaska", "Aeromexico", "Volaris"]
airports = ["PDX", "GDL", "SJC", "LAX", "JFK"]
genders = ["male", "female", "unspecified", "undisclosed"]
reasons = ["On vacation/Pleasure", "Business/Work", "Back Home"]
stays = ["Hotel", "Short-term homestay", "Home", "Friend/Family"]
transits = ["Airport cab", "Car rental", "Mobility as a service", "Public Transportation", "Pickup", "Own car"]
tickets = ["Economy", "Business", "First Class"]
connections = [True, False]
carry_on = [True, False]


def cql_stmt_generator(flights_num=100):
    flights_stmt = "INSERT INTO flights(flight_id, airline, from_city, to_city, day, month, year, connection) VALUES ('{}', '{}', '{}', '{}', {}, {}, {}, {});"
    tickets_stmt = "INSERT INTO tickets_by_f_t(ticket_id, flight_id, ticket, checked_bags, carry_on, month, year, day) VALUES ('{}', '{}', '{}', {}, {}, {}, {}, {});"

    flights_from_stmt = "INSERT INTO flights_from(from_city, month, year, flight_id, airline, to_city, day, connection) VALUES ('{}', {}, {}, '{}', '{}', '{}', {}, {});"
    flights_to_stmt = "INSERT INTO flights_to(to_city, month, year, flight_id, airline, from_city, day, connection) VALUES ('{}', {}, {}, '{}', '{}', '{}', {}, {});"
    
    with open(CQL_FILE, "w") as fd:
        # Generate flights
        flights = []
        for i in range(flights_num):
            flight_id = str(uuid.uuid4())
            flights.append(flight_id)

            from_airport = random.choice(airports)
            to_airport = random.choice(airports)
            while from_airport == to_airport:
                to_airport = random.choice(airports)

            date = random_date(datetime.datetime(2013, 1, 1), datetime.datetime(2023, 4, 25))
            
            reason = random.choice(reasons)
            connection = random.choice(connections)
            airline = random.choice(airlines)

            if reason == "Back Home":
                connection = False

            fd.write(flights_stmt.format(flight_id, airline, from_airport, to_airport, date.day, date.month, date.year, connection))
            fd.write('\n')
        fd.write('\n\n')

        # Genetate tickets by flight
        for i in range(flights_num):
            flight_id = flights[i]
            ticket_id = str(uuid.uuid4())

            date = random_date(datetime.datetime(2013, 1, 1), datetime.datetime(2023, 4, 25))

            ticket = random.choice(tickets)
            checked_bags = random.randint(0, 3)
            carry = random.choice(carry_on)
            fd.write(tickets_stmt.format(ticket_id, flight_id, ticket, checked_bags, carry, date.month, date.year, date.day))
            fd.write('\n')
        fd.write('\n\n')

        # Generate flights_from entries
        for i in range(flights_num):
            flight_id = str(uuid.uuid4())
            from_airport = random.choice(airports)
            to_airport = random.choice(airports)
            while from_airport == to_airport:
                to_airport = random.choice(airports)

            date = random_date(datetime.datetime(2013, 1, 1), datetime.datetime(2023, 4, 25))
            airline = random.choice(airlines)
            connection = random.choice(connections)

            fd.write(flights_from_stmt.format(from_airport, date.month, date.year, flight_id, airline, to_airport, date.day, connection))
            fd.write('\n')
        fd.write('\n\n')

        # Generate flights_to entries
        for i in range(flights_num):
            flight_id = str(uuid.uuid4())
            from_airport = random.choice(airports)
            to_airport = random.choice(airports)
            while from_airport == to_airport:
                from_airport = random.choice(airports)

            date = random_date(datetime.datetime(2013, 1, 1), datetime.datetime(2023, 4, 25))
            airline = random.choice(airlines)
            connection = random.choice(connections)

            fd.write(flights_to_stmt.format(to_airport, date.month, date.year, flight_id, airline, from_airport, date.day, connection))
            fd.write('\n')
        fd.write('\n\n')

        # Generate flights by connection

def random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    rand_date = start_date + datetime.timedelta(days=random_number_of_days)
    return rand_date


def main():
    cql_stmt_generator()


if __name__ == "__main__":
    main()