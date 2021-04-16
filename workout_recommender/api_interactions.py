import requests
import json
import html2text
from langdetect import detect

def get_all_workouts(limit=30):
    raw_responce = requests.get(f'https://wger.de/api/v2/exerciseinfo/?format=json&limit={limit}')
    as_text = json.dumps(raw_responce.json(), indent=4)
    parseable = json.loads(as_text)["results"]
    all_workouts = []
    for workout in parseable:
        new_workout = {
            "name": html2text.html2text(workout["name"]).strip(),
            "description": html2text.html2text(workout["description"]).strip()
        }
        try:
            if detect(new_workout["name"]) == "en" and detect(new_workout["description"]) == "en":
                all_workouts.append(new_workout)
        except Exception:
            continue
    return all_workouts
