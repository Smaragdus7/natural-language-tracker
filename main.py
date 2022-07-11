import requests
import os
from datetime import datetime

APP_ID = os.environ.get("APP_ID_N")
API_KEY = os.environ.get("API_KEY_N")
API_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"

SHEETY_API_ENDPOINT = os.environ.get("S_API_ENDPOINT")
SHEETY_TOKEN = os.environ.get("TOKEN_S")

GENDER = "female"
WEIGHT_KG = 54
HEIGHT_CM = 166
AGE = 28

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
    "x-remote-user-id": "0",
}

workout_info = input("Tell me which exercises you did: ")

workout_params = {
 "query": workout_info,
 "gender": GENDER,
 "weight_kg": WEIGHT_KG,
 "height_cm": HEIGHT_CM,
 "age": AGE,
}

response = requests.post(url=API_ENDPOINT, json=workout_params, headers=headers)
response.raise_for_status()
stats = response.json()
print(stats)

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

sheety_headers = {
    "Authorization": f"Bearer {SHEETY_TOKEN}",
}

for exercise in stats["exercises"]:
    sheet_inputs = {
        "hoja1": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheet_response = requests.post(url=SHEETY_API_ENDPOINT, json=sheet_inputs, headers=sheety_headers)
    print(sheet_response.text)
