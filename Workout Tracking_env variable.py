import requests
from datetime import datetime
import os

APP_ID = os.environ.get("APP_ID_NUTRI")            
API_KEY = os.environ.get("API_KEY_NUTRI")
QUERY = input("What your exercise (runing, walking and etc): ")
GENDER = "male"
WEIGHT_KG = 55
HEIGHHT_CM = 168
AGE = 30

# calculate exercise from nutrition API
nutri_exercis_params = {
    "query": QUERY,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHHT_CM,
    "age": AGE
}

nutri_headear = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

nutri_exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

nutri_request = requests.post(url= nutri_exercise_endpoint, json=nutri_exercis_params, headers=nutri_headear)
result = nutri_request.json()
print(f"Nutritionix API call: \n {result} \n")

# Adding date and time data
today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

# Get data from nutrition and store in a variable for write in google sheet

SHEETY_USR = os.environ.get("SHEETY_USR")
sheety_endpoint = f"https://api.sheety.co/{SHEETY_USR}/myExerciseM/workouts"

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }

    #__________________Request API and POST________________________________________

    # Option 1
    #🔓 No authentication
    # With no authentication anyone who knows the URL of your API can access it. This is fine if your data doesn't contain sensitive information.
    """ 
    sheety_response = requests.post(sheety_endpoint, json=sheet_inputs)
    print(sheety_response.text) 
    """

    # Option 2
    # With basic authentication a username and password will be needed to access your API. This uses the HTTP Basic Auth protocol
    """ 
    SHEETY_USR = os.environ.get("SEETY_USR_AUTH_ID") 
    SEETY_PASS = os.environ.get(SHEETY_USR_AUTH_PASS)
    sheet_response = requests.post(
        sheety_endpoint,
        json=sheet_inputs,
        auth=(
            SHEETY_USR,
            SEETY_PASS,
        )
    )
    """ 
    
    # Option 3
    # With Bearer Token Authentication
    BEARER_TOKEN = os.environ.get("SHEETY_BEARER_TOKEN")
    sheety_bearer_header = {
        "Authorization": f"Bearer {BEARER_TOKEN}"
    }
    
    sheet_response = requests.post(
        sheety_endpoint,
        json=sheet_inputs,
        headers= sheety_bearer_header
    )
    print(sheet_response.text)

