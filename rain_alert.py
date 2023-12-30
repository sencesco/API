import requests
import datetime
from twilio.rest import Client
import os

""" 
__________________This is show API Key tracking with Unauthorized ______________________________________________

API_key = "Your API Key"
APP_ID = "Your APP ID"
# https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude={part}&appid={API key}
OWM_Endpoint ="https://api.openweathermap.org/data/3.0/onecall"
weather_params = {
    "lat": 13.912520,
    "lon": 100.498138,
    "exclude": "hourly"
    "appid": API_key
}

w_request = requests.get(OWM_Endpoint, params=weather_params)
w_request.raise_for_status()    # Output: requests.exceptions.HTTPError: 401 Client Error: Unauthorized 
                                #           for url: https://api.openweathermap.org/data/3.0/onecall?lat=13.91252&
                                #           lon=100.498138&appid={APP_ID}
                                
This web site  not free forcast at all so  then  return HTTPError: 401 Client Error: Unauthorized 

but for still  get sms alert we use https://open-meteo.com/ instead and this website not have an  API key for free plan                             
 """

account_sid = 'Your accoun ID'
auth_token = 'Your Aut Token'

w_request = requests.get("https://api.open-meteo.com/v1/forecast?latitude=13.913&longitude=104.134834&hourly=rain")
w_request.raise_for_status() 
print(w_request)    #<Response [200]>  >> already connected

weather_data = w_request.json()     # can copy json data and convert in here https://jsonviewer.stack.hu/ for easier to visualize
weather_rain = weather_data["hourly"]["rain"]
weather_date = [date.split('T')[0] for date in weather_data['hourly']['time']]

time_now = datetime.datetime.now()
time_now_date = time_now.date()
time_now_hour = time_now.hour
  
will_rain = False 
for index, rain in enumerate(weather_rain):
    if rain > 0 and weather_date[index] == str(time_now_date):
        print(weather_date[index] == str(time_now_date))
        will_rain = True

if will_rain:
        client = Client(account_sid, auth_token)

        message = client.messages.create(
        body="It's going to rain today. Remember to bring an umbrella",
        from_='Twilio test number',
        to='Yourpone or reciever number'
        )
        print(message.status)


