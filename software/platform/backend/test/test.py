#!/usr/bin/env python3

import requests

r = requests.post(
	"http://127.0.0.1:8080/api/manage/teams",
	data={"name": "foo3", "password": "bar"}
)
print(r.status_code)
