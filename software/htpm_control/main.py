#!/usr/bin/env python3

import pigpio
import time
from protocol import *

pigpio.exceptions = False
PI = pigpio.pi()
BUS = 1

# Seconds between each setup test item.
SETUP_DELAY = 1

# Seconds between each individual module test.
MODULE_TEST_DELAY = 5

# Seconds between each individual power line test.
POWER_LINE_TEST_DELAY = 0.5

def main():

	devices = []

	print("--[ HTP!m CONTROL ]--")
	print("This program is meant to be run in the background. Interaction is")
	print("intended to be done entirely via the physical HTP!m CONTROL unit itself.")
	print("This management program will output logs to the terminal.")
	print("------------------------------------------------------------------------")

	# Detect devices.
	print(":: Detecting modules...")
	for addr in range(0x08, 0x79):
		handle = PI.i2c_open(BUS, addr)
		byte = PI.i2c_read_byte(handle)
		if byte >= 0:
			print(f":: | Address: 0x{addr:02x}")
			devices.append(addr)
		PI.i2c_close(handle)

	print(f":: Detected {len(devices)} module(s) over I2C.")
	time.sleep(SETUP_DELAY)

	print(":: Sending a ping to all modules.")
	responded = []
	for addr in devices:
		ack = Ping.send(PI, BUS, addr, 0)
		if ack == False:
			print(f":: | Module 0x{addr:02x} NO ACK.")
		else:
			print(f":: | Module 0x{addr:02x} ACK.")
			responded.append(addr)

	devices = sorted(responded)
	time.sleep(SETUP_DELAY)

	print(":: Performing POST of set.")

	print(":: Actuating all lines in all modules.")
	for addr in devices:
		ack = Actuation.send(PI, BUS, addr, 0, 0xFFFF)
		if ack == False:
			print(f":: | Module 0x{addr:02x} NO ACK.")
		else:
			print(f":: | Module 0x{addr:02x} ACK.")

	time.sleep(SETUP_DELAY)

	print(":: Disabling all lines in all modules.")
	for addr in devices:
		ack = Actuation.send(PI, BUS, addr, 0, 0x0000)
		if ack == False:
			print(f":: | Module 0x{addr:02x} NO ACK.")
		else:
			print(f":: | Module 0x{addr:02x} ACK.")

	time.sleep(SETUP_DELAY)

	for addr in devices:
		print(f":: Testing module 0x{addr:02x}.")
		print(":: | Testing all lines.")
		Actuation.send(PI, BUS, addr, 0, 0xFFFF)
		time.sleep(MODULE_TEST_DELAY)
		print(":: | Testing individual lines.")
		for i in range(16):
			Actuation.send(PI, BUS, addr, 0, 1 << i)
			time.sleep(POWER_LINE_TEST_DELAY)
		Actuation.send(PI, BUS, addr, 0, 0x0000)

	time.sleep(SETUP_DELAY)
	print(":: POST complete. Entering normal operation.")
	print("------------------------------------------------------------------------")

if __name__ == "__main__":
	main()
