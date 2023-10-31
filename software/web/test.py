#!/usr/bin/env python3

import json
import multiprocessing
import requests
import time

from termcolor import colored

from app import *

success = lambda s: print(f"{termcolor('•','green',attrs=['bold'])} {s}")
failure = lambda s: print(f"{termcolor('•','red',attrs=['bold'])} {s}")

def run_tests():

	# [(passed, name), ...]
	results = []

	with requests.Session() as s:
		r = s.post(
			"http://127.0.01:8080/login",
			data={"username": "admin", "password": "12345678"}
		)
		cookies = r.cookies

		r = s.post(
			"http://127.0.01:8080/api/manage/teams",
			cookies=cookies,
			data={"action": "create", "username": "player", "password": "foobar123"}
		)
		if json.loads(r.text)["Status"] == "Success!":
			success("Login successful.")

		r = s.get(
			"http://127.0.01:8080/api/manage/teams",
			cookies=cookies,
		)
		print(r.status_code)
		print(r.text)

def main():

	print("Make sure the server is started before running the tests. You may")
	print("also want to wipe the database.")

	try:
		print("Starting tests.")
		run_tests()
		print("Tests completed.")
	except Exception as e:
		print(e)
		return

if __name__ == "__main__":
	main()
