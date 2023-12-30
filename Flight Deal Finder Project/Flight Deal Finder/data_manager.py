import requests

class DataManager:
    def __init__(self, sheety_usr, sheety_bearer_flight_PJ):
        self.sheety_usr = sheety_usr
        self.sheety_endpoint = f"https://api.sheety.co/{self.sheety_usr}/flightDeals/prices"  
        self.sheety_bearer = {
            "Authorization": f"Bearer {sheety_bearer_flight_PJ}"
        }

    def get_info(self):
        self.sheety_respond = requests.get(self.sheety_endpoint, headers=self.sheety_bearer)
        self.info = self.sheety_respond.json()["prices"]
        print(self.info)
        
    def update_iata_code(self, iata_code_de, iata_code_des, row_id):
        sheety_endpoint_update = f"{self.sheety_endpoint}/{row_id}"
        sheet_inputs_iata = {
            "price": {
                "iataCodeDepart": iata_code_de,
                "iataCodeDestination": iata_code_des,
            }
        }
        self.sheety_post = requests.put(sheety_endpoint_update, json=sheet_inputs_iata, headers=self.sheety_bearer)
        
    def update_price_and_linked(self,lowest_price, linked, row_id):
        sheety_endpoint_update = f"{self.sheety_endpoint}/{row_id}"
        sheet_inputs_price = {
            "price": {
                "lowestPrice(usd)": lowest_price,
                "linked": linked
            }
        }
        self.sheety_update  = requests.put(sheety_endpoint_update, json=sheet_inputs_price, headers=self.sheety_bearer)
        
    
        