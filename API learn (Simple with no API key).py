#In Python we need to call requst library to get request an API
import requests

# use request.get() to request API
request_api = requests.get(url="http://api.open-notify.org/iss-now.json")
print(request_api.status_code)  # Output: 200 is meaning is success

respone_api = requests.get(url="http://open-notify.org/Open-Notify-API/ISs-Location-Now/")
print(respone_api.status_code)  # Output: 404 is meaning is Not found

# Read a json file
data = request_api.json()
print(data)
# We can also acces like this
lat = data["iss_position"]["latitude"]
print(lat)
data_lat = request_api.json()["iss_position"]["latitude"]
print(data_lat)

long = data["iss_position"]["longitude"]
print(long)
data_long = request_api.json()["iss_position"]["longitude"]
print(data_long)

# Manange in a tuple format
iss_position = (lat,long)
print(iss_position)

respone_api = requests.get(url="http://open-notify.org/Open-Notify-API/ISs-Location-Now/")
print(respone_api.status_code)  # Output: 404 is meaning is Not found

#_______ If other that we can raise the exception likee a codee below __________
""" 
if respone.status_code != 200:
    raise Exception("Bad respone from ISS API") 
if respone.status_code == 404:
    raise Exception("That resource deos not exist.")
elif respone.status_code == 401:
    raise Exception("You are not authorised to acces this data.") 

# But this module can call a respone by raise the exception like a code below
respone_appi.raise_for_status() # Output exceptions.HTTPError: 404 Client Error: Not Found for url: 
                        # http://open-notify.org/Open-Notify-API/ISs-Location-Now/
"""

