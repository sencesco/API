import requests
import datetime
import smtplib
import time

my_latitude = 13.912520
my_longtitude = 100.498140
my_email = "Yourmail@gmail.com"
password = "YpurApp_pass"
stmp_mail_client = "smtp.gmail.com"

def is_iss_overhead():
    # This API is no parameter
    request_iss = requests.get("http://api.open-notify.org/iss-now.json")
    request_iss.raise_for_status()
    data = request_iss.json()
    iss_latitude = float(data["iss_position"]["latitude"]) 
    iss_longtitude = float(data["iss_position"]["longitude"]) 
    # Check if The International Space Station is overhead
    # Your position is within +5 or -5 degrees of the iss position.
    if my_latitude <= iss_latitude <= my_latitude+5 and my_longtitude <= iss_longtitude <= my_longtitude+5:
        return True   
     
def is_night():    
    parameter_sun = {
        "lat": my_latitude,
        "lng": my_longtitude,
        # formatted is default is 1:  1 is 12 with AM,PM and 0 is 24hour format
        "formatted":0
    }
    # This API requires a parameter.
    request_sun = requests.get("https://api.sunrise-sunset.org/json", params=parameter_sun)
    request_sun.raise_for_status()
    data_sun = request_sun.json()
    # But we need to compare a hour so
    sunrise = int(data_sun["results"]["sunrise"].split("T")[1].split(":")[0]) # The hour of sunrise
    sunset = int(data_sun["results"]["sunset"].split("T")[1].split(":")[0])   # The hour of sunset
    
    time_now = datetime.datetime.now().hour
    # It's a dark
    if time_now >= sunset or time_now <= sunrise:
        return True

# When run a program The code will run until we closed a computer
while True:
    # Will run in every 60 second 
    time.sleep(60)    
    if is_iss_overhead() and is_night:
        with smtplib.SMTP(stmp_mail_client) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email, 
                to_addrs="reciever@gmail.com", 
                msg=f"Subject: Look up iss crossing you\n\nThe International Space Station is above you in the sky now."
            ) 

     
# print(data_sun) # Output will return not arrang format for easy to see

# So this API have a way to arrang like
# https://api.sunrise-sunset.org/json?lat=36.7201600&lng=-4.4203400
# And replace our latitude and longtitude to here and open by browser and chosen a key that we want so like here
# https://api.sunrise-sunset.org/json?lat=13.9125200&lng=100.498140

# sunrise = data_sun["results"]["sunrise"] # Print output: 2023-08-24T23:04:46+00:00 
# sunset = data_sun["results"]["sunset"]   # Print output: 2023-08-25T11:35:44+00:00

# So the unique time  it seem hard to see so will use string.split() for easy to see and mangae it
# sunrise = sunrise.split("T")[1].split("+")[0]
# print(sunrise)
# time_now = datetime.datetime.now()
# print(time_now)
