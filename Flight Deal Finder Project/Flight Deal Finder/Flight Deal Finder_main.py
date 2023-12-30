from data_manager import DataManager
from flight_management import FlightSearch
from notification_manager import NotificationManager
from datetime import datetime, timedelta

EMAIL = "Yourmail@gmail.com";    EMAIL_PASS = "YourApp_pas";    RECEIVER = "receiver@gmail.com"

SHEETY_USR = "SHEETY_USR"
SHEETY_BEARER_TOKEN_FLIGHT_PJ = "SHEETY_BEARER_TOKEN_FLIGHT_P" 

FLIGHT_API_KEY = "FLIGHT_API_KEY"

flight_inf = DataManager(SHEETY_USR,SHEETY_BEARER_TOKEN_FLIGHT_PJ)
flight_mgn = FlightSearch(FLIGHT_API_KEY)
notification_mail = NotificationManager(EMAIL,EMAIL_PASS, RECEIVER)

flight_inf.get_info()
tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

# len not sutract -1 becuase sheety API json file data start from row id = 2
for i in range(len(flight_inf.info)):
    dep = flight_inf.info[i]["departCity"]
    des = flight_inf.info[i]["destinationCity"]
    lw_price = flight_inf.info[i]["lowestPrice(usd)"]
    row_id = flight_inf.info[i]["id"]
    # Search and update IATA city code
    if flight_inf.info[i]["iataCodeDepart"] == "" or flight_inf.info[i]["iataCodeDestination"] == "":
        print("Updating IATA code")
        dep_decode = flight_mgn.destination_code_iata(dep)
        des_decode = flight_mgn.destination_code_iata(des)   
        flight_inf.update_iata_code(dep_decode,des_decode,row_id)        
        print("IATA code is update succesfully")
        
    flight = flight_mgn.search_flight(
        flight_inf.info[i]["iataCodeDepart"],   flight_inf.info[i]["iataCodeDestination"],
        tomorrow,   six_month_from_today,   dep,    des
        )
    # If search not found flight.price=None, if not use try an except will always return AttributeError
    try: 
        if flight.price < lw_price:
            notification_mail.send_mail(
                subject="Flight Deal Lower price",
                content=f"""
                Low price alert! Only ${flight.price} to fly from 
                {flight.depart_city}-{flight.depart_airport} to {flight.destination_city}-{flight.destination_airport},
                from {flight.out_date} to {flight.return_date}.
                Ticket linked: {flight.ticket_linked} 
                """
            )
            flight_inf.update_price_and_linked(flight.price, flight.ticket_linked, row_id)
    except AttributeError:
        pass



 