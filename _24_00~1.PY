
import json
from datetime import datetime
import requests
import os
import time

# set up environment variables:
APP_ID = os.environ.get('APP_ID', 'APP_ID does not exist')
API_KEY = os.environ.get('API_KEY', 'API_KEY does not exist')
AUTHORIZATION_BEARER_TOKEN = os.environ.get('AUTHORIZATION_BEARER_TOKEN', 'AUTHORIZATION_BEARER_TOKEN does not exist')
EXERCISE_ENDPOINT_URL = os.environ.get('EXERCISE_ENDPOINT_URL', 'EXERCISE_ENDPOINT_URL does not exist')
SHEETY_ENDPOINT_URL = os.environ.get('SHEETY_ENDPOINT_URL', 'SHEETY_ENDPOINT_URL does not exist')

print(f"The APP_ID is: {APP_ID}")
print(f"The API_KEY is: {API_KEY}")
print(f"The AUTHORIZATION_BEARER_TOKEN is: {AUTHORIZATION_BEARER_TOKEN}")

gender = "male"
weight_in_kg = "75.8"
height_in_cm = "179"
age = 40

#------------------ Nutritionix Territory -----------------#
exercise_endpoint_url = EXERCISE_ENDPOINT_URL

#-----------------  Sheety Territory -----------------#
sheety_endpoint_url = SHEETY_ENDPOINT_URL

# to use bearer Tokens:
sheety_headers = {
    "Authorization": f"Bearer {AUTHORIZATION_BEARER_TOKEN}",
    "Content-Type": "application/json"
}

exercise_text = input("Please tell me which exercises you did Today, and the duration of each (if you know): ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}
print(APP_ID)
print(API_KEY)


parameters = {
    "query": exercise_text,
    "gender": gender,
    "weight_kg": weight_in_kg,
    "height_cm": height_in_cm,
    "age": age,
}

exercise_response = requests.post(url=exercise_endpoint_url, json=parameters, headers=headers)
exercise_result = exercise_response.json()
print(exercise_result)

date_and_time_now = datetime.now()
print(date_and_time_now)

now_formatted_date = date_and_time_now.strftime("%d/%m/%Y")
print(now_formatted_date)

now_formatted_time = date_and_time_now.strftime("%H:%M:%S")
print(now_formatted_time)


for each_exercise in exercise_result['exercises']:
    json_payload_sheet_inputs = {
        'workout' : {
            "date" : now_formatted_date,
            "time" : now_formatted_time,
            "exercise": each_exercise['name'].title(),
            "duration": each_exercise['duration_min'],
            "calories": each_exercise['nf_calories'],
        }
    }
    sheety_post_request_response = requests.post(url=sheety_endpoint_url, json=json_payload_sheet_inputs, headers=sheety_headers)
    print(sheety_post_request_response.text)
