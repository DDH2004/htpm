#!/usr/bin/env python3

import json
import requests

from termcolor import colored

success = lambda s: print(f"{colored('●','green',attrs=['bold'])} {s}")
failure = lambda s: print(f"{colored('●','red',attrs=['bold'])} {s}")

def run_tests():

	with requests.Session() as s:

		# Test login.

		r = s.post(
			"http://127.0.0.1:8080/login",
			data={"username": "admin", "password": "12345678"},
			allow_redirects=False,
		)
		cookies = r.cookies

		f = failure
		if r.status_code == 302:
			f = success

		f("Login")
		print()

		# Test create team.

		r = s.post(
			"http://127.0.0.1:8080/api/manage/teams",
			cookies=cookies,
			data={"action": "create", "username": "Alpha", "password": "foobar123"}
		)
		r = s.get(
			"http://127.0.0.1:8080/api/manage/teams",
			cookies=cookies,
		)
		f = failure
		if (j:=json.loads(r.text))["Status"] == "Success!" and [2,"Alpha","foobar123"] in j["Teams"]:
			f = success

		f("POST /api/manage/teams (create)")
		f("GET  /api/manage/teams (read)")

		# Test update team.

		r = s.post(
			"http://127.0.0.1:8080/api/manage/teams",
			cookies=cookies,
			data={"action": "update", "username": "Alpha", "newUsername": "Bravo", "newPassword": "foobar321"}
		)
		r = s.get(
			"http://127.0.0.1:8080/api/manage/teams",
			cookies=cookies,
		)
		f = failure
		if (j:=json.loads(r.text))["Status"] == "Success!" and [2,"Bravo","foobar321"] in j["Teams"]:
			f = success

		f("POST /api/manage/teams (update)")

		# Test delete team.

		r = s.post(
			"http://127.0.0.1:8080/api/manage/teams",
			cookies=cookies,
			data={"action": "delete", "username": "Bravo"}
		)
		r = s.get(
			"http://127.0.0.1:8080/api/manage/teams",
			cookies=cookies,
		)
		f = failure
		if (j:=json.loads(r.text))["Status"] == "Success!" and [2,"Bravo","foobar321"] not in j["Teams"]:
			f = success

		f("POST /api/manage/teams (delete)")
		print()

		# Test create player.

		r = s.post(
			"http://127.0.0.1:8080/api/manage/teams",
			cookies=cookies,
			data={"action": "create", "username": "Alpha", "password": "foobar123"}
		)
		r = s.post(
			"http://127.0.0.1:8080/api/manage/players",
			cookies=cookies,
			data={"action": "create", "team": "Alpha", "name": "John Doe"}
		)
		r = s.get(
			"http://127.0.0.1:8080/api/manage/players",
			cookies=cookies,
		)
		f = failure
		if (j:=json.loads(r.text))["Status"] == "Success!" and [2,"John Doe"] in j["Players"]:
			f = success

		f("POST /api/manage/players (create)")
		f("GET  /api/manage/players (read)")

		# Test update player.

		r = s.post(
			"http://127.0.0.1:8080/api/manage/players",
			cookies=cookies,
			data={"action": "update", "team": "Alpha", "name": "John Doe", "newTeam": "Alpha", "newName": "Jane Doe"}
		)
		r = s.get(
			"http://127.0.0.1:8080/api/manage/players",
			cookies=cookies,
		)
		f = failure
		if (j:=json.loads(r.text))["Status"] == "Success!" and [2,"Jane Doe"] in j["Players"]:
			f = success

		f("POST /api/manage/players (update)")

		# Test delete player.

		r = s.post(
			"http://127.0.0.1:8080/api/manage/players",
			cookies=cookies,
			data={"action": "delete", "team": "Alpha", "name": "Jane Doe"}
		)
		r = s.get(
			"http://127.0.0.1:8080/api/manage/players",
			cookies=cookies,
		)
		f = failure
		if (j:=json.loads(r.text))["Status"] == "Success!" and [2,"Jane Doe"] not in j["Players"]:
			f = success

		f("POST /api/manage/players (delete)")
		print()

		# Test create challenge.

		r = s.post(
			"http://127.0.0.1:8080/api/manage/challenges",
			cookies=cookies,
			data={"action": "create", "title": "Challenge A"}
		)
		r = s.get(
			"http://127.0.0.1:8080/api/manage/challenges",
			cookies=cookies,
		)
		f = failure
		if (j:=json.loads(r.text))["Status"] == "Success!" and "Challenge A" in j["Challenges"]:
			f = success

		f("POST /api/manage/challenges (create)")
		f("GET  /api/manage/challenges (read)")

		# Test update challenge.

		r = s.post(
			"http://127.0.0.1:8080/api/manage/challenges",
			cookies=cookies,
			data={"action": "update", "title": "Challenge A", "newTitle": "Challenge Alpha"}
		)
		r = s.get(
			"http://127.0.0.1:8080/api/manage/challenges",
			cookies=cookies,
		)
		f = failure
		if (j:=json.loads(r.text))["Status"] == "Success!" and "Challenge Alpha" in j["Challenges"]:
			f = success

		f("POST /api/manage/challenges (update)")

		# Test delete challenge.

		r = s.post(
			"http://127.0.0.1:8080/api/manage/challenges",
			cookies=cookies,
			data={"action": "delete", "title": "Challenge Alpha"}
		)
		r = s.get(
			"http://127.0.0.1:8080/api/manage/challenges",
			cookies=cookies,
		)
		f = failure
		if (j:=json.loads(r.text))["Status"] == "Success!" and "Challenge Alpha" not in j["Challenges"]:
			f = success

		f("POST /api/manage/challenges (delete)")
		print()

		# Test create solve.

		r = s.post(
			"http://127.0.0.1:8080/api/manage/challenges",
			cookies=cookies,
			data={"action": "create", "title": "Challenge A"}
		)
		r = s.post(
			"http://127.0.0.1:8080/api/manage/solves",
			cookies=cookies,
			data={"action": "create", "team": "Alpha", "challenge": "Challenge A"}
		)
		r = s.get(
			"http://127.0.0.1:8080/api/manage/solves",
			cookies=cookies,
		)
		f = failure
		if (j:=json.loads(r.text))["Status"] == "Success!":
			for solve in j["Solves"]:
				if 2 in solve and 1 in solve:
					f = success
					break

		f("POST /api/manage/solves (create)")
		f("POST /api/manage/solves (read)")

		# Test update solve.

		r = s.post(
			"http://127.0.0.1:8080/api/manage/teams",
			cookies=cookies,
			data={"action": "create", "username": "Bravo", "password": "foobar123"}
		)
		r = s.post(
			"http://127.0.0.1:8080/api/manage/challenges",
			cookies=cookies,
			data={"action": "create", "title": "Challenge B"}
		)
		r = s.post(
			"http://127.0.0.1:8080/api/manage/solves",
			cookies=cookies,
			data={
				"action": "update",
				"team": "Alpha", "challenge": "Challenge A",
				"newTeam": "Bravo", "newChallenge": "Challenge B"
			}
		)
		r = s.get(
			"http://127.0.0.1:8080/api/manage/solves",
			cookies=cookies,
		)
		f = failure
		if (j:=json.loads(r.text))["Status"] == "Success!":
			for solve in j["Solves"]:
				if 3 in solve and 2 in solve:
					f = success
					break

		f("POST /api/manage/solves (update)")

		# Test delete solve.

		r = s.post(
			"http://127.0.0.1:8080/api/manage/solves",
			cookies=cookies,
			data={"action": "delete", "team": "Bravo", "challenge": "Challenge B"}
		)
		r = s.get(
			"http://127.0.0.1:8080/api/manage/solves",
			cookies=cookies,
		)
		f = success
		if (j:=json.loads(r.text))["Status"] == "Success!":
			for solve in j["Solves"]:
				if 3 in solve and 2 in solve:
					f = failure
					break

		f("POST /api/manage/solves (delete)")

def main():

	print("Make sure the server is started before running the tests. You may")
	print("also want to wipe the database.")
	print()

	try:
		print("Tests:\n")
		run_tests()
		print()
		print("Tests completed.")
	except Exception as e:
		print(e)
		return

if __name__ == "__main__":
	main()
