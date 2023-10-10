import json
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

def read() -> bool:

    r = requests.get(
        "http://localhost:8080/api/manage/teams",
    )

    if r.status_code != 200:
        print(f"API returned an HTTP {r.status_code}, expected 200.")
        return False

    if r.content != b'{"Status":"Success!","Teams":["Foobar"]}\n':
        print("API returned:")
        print(r.content)
        print("Expected:")
        print(b'{"Status":"Success!","Teams":["Foobar"]}\n')

    return True

def update(name: str, newName: str, newPassword: str) -> bool:

    r = requests.post(
        "http://localhost:8080/api/manage/teams",
        data={
            "action": "update",
            "name": name,
            "newName": newName,
            "newPassword": newPassword 
        }
    )

    if r.status_code != 200:
        print(f"API returned an HTTP {r.status_code}, expected 200.")
        return False

    return True
