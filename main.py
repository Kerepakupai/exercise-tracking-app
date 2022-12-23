import requests
import os
from datetime import datetime
from requests.auth import HTTPBasicAuth


GENDER = "male"
WEIGHT_KG = "94"
HEIGHT_CM = "172"
AGE = "40"

APP_ID = os.environ["ENV_NIX_APP_ID"]
APP_KEY = os.environ["ENV_NIX_API_KEY"]

headers = {
    "x-app-id": APP_ID,
    "x-app-key": APP_KEY,
    "x-remote-user-id": "0",
}
parameters = {
    "query": input("Tell me which exercises you did: "),
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}
natural_exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
response = requests.post(
    url=natural_exercise_endpoint,
    json=parameters,
    headers=headers
)
today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%H:%M:%S")

exercises = response.json()["exercises"]

for exercise in exercises:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    sheety_endpoint = os.environ["ENV_SHEETY_ENDPOINT"]
    sheety_username = os.environ["ENV_SHEETY_USERNAME"]
    sheety_password = os.environ["ENV_SHEETY_PASSWORD"]

    sheet_auth = HTTPBasicAuth(sheety_username, sheety_password)
    sheet_response = requests.post(url=sheety_endpoint, json=sheet_inputs, auth=sheet_auth)
    print(sheet_response .json())
