class Message:

	preamble  = None
	length    = None
	data      = None
	crc       = None
	end       = None

	def __init__(self, content: bytearray):
		self.preamble  = content[0:3]
		self.length    = content[3]
		self.data      = content[4:4+self.length]
		self.crc       = content[4+self.length]
		self.end       = content[-3:]

	def __str__(self):

		formatted  = "--[ MESSAGE ]--\n"
		formatted += f"Preamble  : 0x{self.preamble.hex()}\n"
		formatted += f"Length    : 0x{self.length:02X}\n"

		if self.length != 0x00:
			formatted += f"Data      : 0x{self.data.hex()}\n"
		else:
			formatted += f"Data      : <empty>\n"

		if self._validate():
			formatted += f"CRC-8     : 0x{self.crc:02X} (valid)\n"
		else:
			formatted += f"CRC-8     : 0x{self.crc:02X} (invalid)\n"

		formatted += f"End       : 0x{self.end.hex()}"

		return formatted

	def _validate(self) -> bool:

		data = [self.length, *self.data]
		return Message.crc8(data) == self.crc

	def crc8(data: list):
		
		crc = 0
		for i in range(len(data)):
			crc ^= data[i]
			for j in range(8):
				crc &= 0xFF
				if crc & 0x80:
					crc = (crc << 1) ^ 0x07
				else:
					crc <<= 1

		return crc

	def make(data) -> bytearray:
		return bytearray([
			0x33, 0x79, 0x20,
			len(data),
			*data,
			Message.crc8([len(data), *data]),
			0x20, 0x79, 0x33
		])

	def bytes(self) -> list:
		return [
			*self.preamble,
			self.length,
			*self.data,
			self.crc,
			*self.end
		]

class Ping(Message):

	mtype  = None
	mid    = None
	src    = None
	dst    = None

	def __init__(self, mid: int, src: int, dst: int):
		self.mtype  = 1
		self.mid    = mid
		self.src    = src
		self.dst    = dst
		super().__init__(Message.make([self.mtype, self.mid, self.src, self.dst]))

	def info(self):
		print(f"MTYPE  : {self.mtype} (PING)")
		print(f"MID    : {self.mid}")
		print(f"SRC    : {self.src}")
		print(f"DST    : {self.dst}")

class Ack(Message):

	mtype  = None
	mid    = None
	src    = None
	dst    = None
	ver    = None

	def __init__(self, mid: int, src: int, dst: int, ver: int):
		self.mtype  = 2
		self.mid    = mid
		self.src    = src
		self.dst    = dst
		self.ver    = ver
		super().__init__(Message.make([
			self.mtype, self.mid, self.src, self.dst, self.ver]))

	def info(self):
		print(f"MTYPE  : {self.mtype} (ACK)")
		print(f"MID    : {self.mid}")
		print(f"SRC    : {self.src}")
		print(f"DST    : {self.dst}")
		print(f"VER    : {self.ver}")

