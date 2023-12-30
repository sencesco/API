class FlightData:
    
    def __init__(self, price, depart_city, depart_airport, destination_city, destination_airport, out_date, return_date, ticket_linked):
        self.price = price
        self.depart_city = depart_city
        self.depart_airport = depart_airport
        self.destination_city = destination_city
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date
        self.ticket_linked = ticket_linked