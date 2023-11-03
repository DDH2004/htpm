#!/usr/bin/env python3

import socket
import time
from datetime import datetime
from threading import Thread

from secrets import *

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

def handle(client, address):

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

		elif words[1] == IDENTITY_WORD["t1-htpm-t0"]:
			print("Status update from Railroad.")
			state["t1-htpm-t0"] = str(words[2])

		elif words[1] == IDENTITY_WORD["t2-htpm-t0"]:
			print("Status update from Power Grid.")
			state["t2-htpm-t0"] = str(words[2])

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

	with socket.socket() as s:
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		print(":: Listening on 0.0.0.0:8891.")
		s.bind(("0.0.0.0", 8891))
		s.listen()
		while True:
			c, addr = s.accept()
			Thread(target=handle, args=(c,addr), daemon=True).start()

if __name__ == "__main__":
	main()
