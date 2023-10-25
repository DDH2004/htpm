from smbus import SMBus

class I2C:

	bus = None

	def __init__(self, line=1):
		self.bus = SMBus(line)

	def send(self, address: int, data: list):
		self.bus.write_i2c_block_data(address, 0, data)

