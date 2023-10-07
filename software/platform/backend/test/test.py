#!/usr/bin/env python3

import requests

r = requests.post(
	"http://127.0.0.1:8080/api/manage/teams",
	data={"action": "delete", "name": "bar"}
)
print(r.status_code)
print(r.content)
