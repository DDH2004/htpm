#!/usr/bin/env python3

import json
import requests
import socket
import time
from datetime import datetime
from getpass import getpass
from threading import Thread

from secrets import *

ENDPOINT = "https://htpm23.shawnd.xyz"

state = {
	"t0-htpm-t0": "NULL",
	"t1-htpm-t0": "NULL",
	"t2-htpm-t0": "NULL",
}

def format_state():

	output = ""

	output += f"t0-htpm-t0 {state['t0-htpm-t0']}\n"
	output += f"t1-htpm-t0 {state['t1-htpm-t0']}\n"
	output += f"t2-htpm-t0 {state['t2-htpm-t0']}\n"

	return output.encode()

def reward(challenge, data, password):

	r = requests.post(
		ENDPOINT+"/login",
		data={"username": "admin", "password": password},
		allow_redirects=False,
	)
	cookies = r.cookies

	r = requests.get(
		ENDPOINT+"/api/manage/teams",
		cookies=cookies
	)
	j = json.loads(r.text)

	teams = []

	for team in j["Teams"]:
		teams.append(team[1])

	for line in data.split("\n"):
		for team in teams:
			if f"team {team.lower()} was here" in line.lower():
				r = requests.post(
					ENDPOINT+"/api/manage/solves",
					data={
						"action": "create",
						"team": team, "challenge": challenge
					},
					cookies=cookies,
				)
				if r.status_code == 200:
					print(f"Rewarded team {team} for solving {challenge}.")

def handle(client, address, password):

	global state

	print(f"\n\n:: Received connection from {address[0]}:{address[1]}.")
	print(datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))

	try:
		data = client.recv(4096).decode("utf-8")
		words = data.split()

		print(f"Received:\n---\n{data}---")

		assert words[0] == AUTH_WORD, "Bad auth word."

		if words[1] == IDENTITY_WORD["t0-htpm-t0"]:
			print("Status update from Smart Home.")
			state["t0-htpm-t0"] = str(words[2])
			reward("Smart House", data, password)

		elif words[1] == IDENTITY_WORD["t1-htpm-t0"]:
			print("Status update from Railroad.")
			state["t1-htpm-t0"] = str(words[2])
			reward("Railroad", data, password)

		elif words[1] == IDENTITY_WORD["t2-htpm-t0"]:
			print("Status update from Power Grid.")
			state["t2-htpm-t0"] = str(words[2])
			reward("Power Grid", data, password)

		elif words[1] == IDENTITY_WORD["retrieval"]:
			print("Retrieval request.")
			client.send(format_state())

		else:
			raise Exception(f"Unknown identity word: {words[1]}")

	except Exception as e:
		print(f"Exception: {e}")
	finally:
		client.close()

def main():

	password = getpass("[login] password for admin: ")

	with socket.socket() as s:
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		print(":: Listening on 0.0.0.0:8891.")
		s.bind(("0.0.0.0", 8891))
		s.listen()
		while True:
			c, addr = s.accept()
			Thread(target=handle, args=(c,addr,password), daemon=True).start()

if __name__ == "__main__":
	main()
