#!/usr/bin/env python3

import random
import socket
import time

from secrets import *

def main():

	while True:

		with open("/app/states/notes.txt", "r") as f:
			notes = f.read()

		with open("/app/states/lights.txt", "r") as f:
			lights = f.read()

		state = f"{lights}\n{notes}".encode()

		message = f"{AUTH_WORD} {IDENTITY_WORD} {state}"

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect(("htpm23.shawnd.xyz", 8891))
		s.send(state)
		s.close()

		time.sleep(random.uniform(0, 5))

if __name__ == "__main__":
	main()
