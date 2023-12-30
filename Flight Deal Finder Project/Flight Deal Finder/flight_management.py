import requests
from flight_data import FlightData

class FlightSearch:
    def __init__(self,apikey):
        self.flight_API_endpoint = "https://api.tequila.kiwi.com"
        self.flight_header = {
        "apikey": apikey
        }

    # Search city code
    def destination_code_iata(self,cityname):
        destination_endpoint = f"{self.flight_API_endpoint}/locations/query"
        destination_params = {
            "term": cityname, 
            "location_types": "city"
        }
        destination_respone = requests.get(destination_endpoint, params=destination_params, headers=self.flight_header)
        self.IATA_code = destination_respone.json()["locations"][0]["code"]
        return self.IATA_code
    
    def search_flight(self,derpart_location, destination_location, from_date, to_date, dep, des):
        flight_search_endpoint = f"{self.flight_API_endpoint}/v2/search"
        flight_search_params = {
            "fly_from": f"city:{derpart_location}",
            "fly_to": f"city:{destination_location}",
            "date_from": from_date.strftime("%d/%m/%Y"),
            "date_to": to_date.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 3,
            "nights_in_dst_to": 15,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "USD"
        }
        flight_search_respone = requests.get(flight_search_endpoint, params=flight_search_params, headers=self.flight_header)
        try:
            data = flight_search_respone.json()["data"][0]
        except IndexError:
            print(f"No flights found for {dep} To {des}.")
            return None
        flight_data = FlightData(
            price=data["price"],
            depart_city=    data["route"][0]["cityFrom"],
            depart_airport= data["route"][0]["flyFrom"],
            destination_city=   data["route"][0]["cityTo"],
            destination_airport=    data["route"][0]["flyTo"],
            out_date=   data["route"][0]["local_departure"].split("T")[0],
            return_date=    data["route"][1]["local_departure"].split("T")[0],
            ticket_linked=  data["deep_link"]
        )
        print(f"From: {flight_data.depart_city} To: {flight_data.destination_city} >> The lowest price is ${flight_data.price}")
        return flight_data
