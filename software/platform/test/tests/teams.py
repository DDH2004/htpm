import requests
from termcolor import colored

def create(name: str, password: str) -> bool:

    r = requests.post(
        "http://localhost:8080/api/manage/teams",
        data={
            "action": "create",
            "name": name,
            "password": password
        }
    )

    if r.status_code != 200:
        print(f"API returned an HTTP {r.status_code}, expected 200.")
        return False

    return True

