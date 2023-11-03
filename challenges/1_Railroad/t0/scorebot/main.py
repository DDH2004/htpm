#!/usr/bin/env python3

import random
import socket
import time

from secrets import *

def main():

	while True:

		try:
			with open("/tmp/velocity.txt", "r") as f:
				velocity = f.read()
			with open("/tmp/note.txt", "r") as f:
				note = f.read()

			message = f"{AUTH_WORD} {IDENTITY_WORD} {velocity}{note}"

			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect(("45.77.0.24", 8891))
			s.send(message.encode())
			s.close()

			time.sleep(random.uniform(0, 10))
		except Exception as e:
			print("Couldn't update status for some reason.")
			print(e)

if __name__ == "__main__":
	main()
