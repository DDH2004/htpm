#!/usr/bin/env python3

def main():

	while True:
		with open("/tmp/velocity.txt", "r") as f:
			velocity = int(f.read())

		print(f"Current speed: {velocity}")
		print("Actions:")
		print("  1. Increase 5 mph")
		print("  2. Decrease 5 mph")
		print()

		action = int(input("> "))

		if velocity >= -95 and velocity <= 95:
			if action == 1:
				with open("/tmp/velocity.txt", "w") as f:
					f.write(str(velocity+5)+"\n")
			elif action == 2:
				with open("/tmp/velocity.txt", "w") as f:
					f.write(str(velocity-5)+"\n")

if __name__ == "__main__":
	main()
