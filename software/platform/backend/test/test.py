#!/usr/bin/env python3

import requests

#r = requests.post(
#	"http://127.0.0.1:8080/api/manage/teams",
#	data={"action": "create", "name": "foo", "password": "bar"}
#)
#print(r.status_code)
#print(r.content)

#r = requests.post(
#	"http://127.0.0.1:8080/api/manage/players",
#	data={"action": "create", "team": 1, "name": "John Doe"}
#)
#print(r.status_code)
#print(r.content)

#r = requests.get(
#	"http://127.0.0.1:8080/api/manage/players",
#)
#print(r.status_code)
#print(r.content)

#r = requests.post(
#	"http://127.0.0.1:8080/api/manage/players",
#	data={"action": "update", "team": 1, "name": "John Doe",
#		"newTeam": 2, "newName": "Jane Doe"}
#)
#print(r.status_code)
#print(r.content)

r = requests.post(
	"http://127.0.0.1:8080/api/manage/players",
	data={"action": "delete", "team": 2, "name": "Jane Doe"}
)
print(r.status_code)
print(r.content)
