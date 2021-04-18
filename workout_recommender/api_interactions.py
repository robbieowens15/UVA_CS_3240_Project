import requests
import json
import html2text
from langdetect import detect

def get_all_muscle_groups():
    raw_responce = requests.get('https://wger.de/api/v2/exercisecategory/?format=json')
    as_text = json.dumps(raw_responce.json(), indent=4)
    parseable = json.loads(as_text)["results"]
    muscle_groups = []
    for muscle_group in parseable:
        new_muscle_group = {
            "id": muscle_group["id"],
            "name": muscle_group["name"].strip()
        }
        muscle_groups.append(new_muscle_group)
    return muscle_groups

def get_select_workouts(limit=30, muscle_group="Any/All"):
    if muscle_group == "Any/All":
        return get_all_workouts(limit=limit)
    else:
        counter = 0
        raw_responce = requests.get(f'https://wger.de/api/v2/exerciseinfo/?format=json&limit=999')
        as_text = json.dumps(raw_responce.json(), indent=4)
        parseable = json.loads(as_text)["results"]
        workouts = []
        for workout in parseable:
            if workout["category"]["name"] == muscle_group:
                new_workout = {
                    "name": html2text.html2text(workout["name"]).strip(),
                    "description": html2text.html2text(workout["description"]).strip()
                }
                try:
                    if detect(new_workout["name"]) == "en" and detect(new_workout["description"]) == "en":
                        workouts.append(new_workout)
                        counter = counter + 1
                except Exception:
                    continue
            if counter == limit:
                break
        return workouts

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
