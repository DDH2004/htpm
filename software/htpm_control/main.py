#!/usr/bin/env python3

from I2C import *
from protocol import *

def main():

	i2c = I2C()

	packet = Tset(0, 1, 2, 10, 100, 500, 200)
	packet.info()
	i2c.send(0x10, packet.bytes())

if __name__ == "__main__":
	main()
