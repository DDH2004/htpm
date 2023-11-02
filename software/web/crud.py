#!/usr/bin/env python3

from requests import get, post
from getpass import getpass

ENDPOINT = "http://127.0.0.1:8080"

def get_action():

	print("Actions:")
	print()
	print(" 0. Quit.")
	print()
	print(" 1. Create a team.")
	print(" 2. Read all teams.")
	print(" 3. Update a team.")
	print(" 4. Delete a team.")
	print()
	print(" 5. Create a player.")
	print(" 6. Read all players.")
	print(" 7. Update a player.")
	print(" 8. Delete a player.")
	print()
	print(" 9. Create a challenge.")
	print("10. Read all challenges.")
	print("11. Update a challenge.")
	print("12. Delete a challenge.")
	print()
	print("13. Create a solve.")
	print("14. Read all solves.")
	print("15. Update a solve.")
	print("16. Delete a solve.")
	print()

	while True:
		action = input("> ")
		try:
			action = int(action)
			assert action >= 0 and action <= 16
			return action
		except:
			pass
		print("Invalid input.")

def do(action: int, cookies: str):

	# Create a team.
	if action == 1:
		username = input("Username: ")
		password = input("Password: ")
		post(
			ENDPOINT+"/api/manage/teams",
			cookies=cookies,
			data={"action": "create", "username": username, "password": password}
		)

	# Read all teams.
	elif action == 2:
		r = get(
			ENDPOINT+"/api/manage/teams",
			cookies=cookies
		)
		print(r.text, end="")

	# Update a team.
	elif action == 3:
		username = input("Username: ")
		newUsername = input("New username: ")
		newPassword = input("New password: ")
		post(
			ENDPOINT+"/api/manage/teams",
			cookies=cookies,
			data={
				"action": "update", "username": username,
				"newUsername": newUsername, "newPassword": newPassword
			}
		)

	# Delete a team.
	elif action == 4:
		username = input("Username: ")
		post(
			ENDPOINT+"/api/manage/teams",
			cookies=cookies,
			data={"action": "delete", "username": username}
		)

	# Create a player.
	elif action == 5:
		team = input("Team name: ")
		name = input("Player name: ")
		post(
			ENDPOINT+"/api/manage/players",
			cookies=cookies,
			data={"action": "create", "team": team, "name": name}
		)

	# Read all players.
	elif action == 6:
		r = get(
			ENDPOINT+"/api/manage/players",
			cookies=cookies
		)
		print(r.text, end="")

	# Update a player.
	elif action == 7:
		team = input("Team name: ")
		name = input("Player name: ")
		newTeam = input("New team name: ")
		newName = input("New player name: ")
		post(
			ENDPOINT+"/api/manage/players",
			cookies=cookies,
			data={
				"action": "update",
				"team": team, "name": name,
				"newTeam": newTeam, "newName": newName
			}
		)

	# Delete a player.
	elif action == 8:
		team = input("Team name: ")
		name = input("Player name: ")
		post(
			ENDPOINT+"/api/manage/players",
			cookies=cookies,
			data={"action": "delete", "team": team, "name": name}
		)

	# Create a challenge.
	elif action == 9:
		title = input("Title: ")
		post(
			ENDPOINT+"/api/manage/challenges",
			cookies=cookies,
			data={"action": "create", "title": title}
		)

	# Read all challenges.
	elif action == 10:
		r = get(
			ENDPOINT+"/api/manage/challenges",
			cookies=cookies
		)
		print(r.text, end="")

	# Update a challenge.
	elif action == 11:
		title = input("Title: ")
		newTitle = input("New title: ")
		post(
			ENDPOINT+"/api/manage/challenges",
			cookies=cookies,
			data={"action": "update", "title": title, "newTitle": newTitle}
		)

	# Delete a challenge.
	elif action == 12:
		title = input("Title: ")
		post(
			ENDPOINT+"/api/manage/challenges",
			cookies=cookies,
			data={"action": "delete", "title": title}
		)

	# Create a solve.
	elif action == 13:
		team = input("Team: ")
		challenge = input("Challenge: ")
		post(
			ENDPOINT+"/api/manage/solves",
			cookies=cookies,
			data={"action": "create", "team": team, "challenge": challenge}
		)

	# Read all solves.
	elif action == 14:
		r = get(
			ENDPOINT+"/api/manage/solves",
			cookies=cookies
		)
		print(r.text, end="")

	# Update a solve.
	elif action == 15:
		team = input("Team: ")
		challenge = input("Challenge: ")
		newTeam = input("New team: ")
		newChallenge = input("New challenge: ")
		post(
			ENDPOINT+"/api/manage/solves",
			cookies=cookies,
			data={
				"action": "update",
				"team": team, "challenge": challenge,
				"newTeam": newTeam, "newChallenge": newChallenge
			}
		)

	# Delete a solve.
	elif action == 16:
		team = input("Team: ")
		challenge = input("Challenge: ")
		post(
			ENDPOINT+"/api/manage/solves",
			cookies=cookies,
			data={"action": "delete", "team": team, "challenge": challenge}
		)

	print("\nDone.")

def main():

	password = getpass("[login] password for admin: ")

	r = post(
		"http://127.0.0.1:8080/login",
		data={"username": "admin", "password": password},
		allow_redirects=False,
	)
	cookies = r.cookies

	while True:
		try:
			action = get_action()
			if action == 0:
				return
			do(action, cookies)
		except:
			pass
		print("\n" + "-"*64 + "\n")

if __name__ == "__main__":
	main()
