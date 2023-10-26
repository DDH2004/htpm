import time

# MTYPE values
PING = 0
ACK = 1
ACTUATION = 2
TMASK = 3
TSET = 4

class Message:

	preamble  = None
	length    = None
	data      = None
	crc       = None
	end       = None

	def __init__(self, content: bytes):
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

	def from_bytes(content: bytes):
		"""
		Return a particular Message child type given raw content bytes. Return
		False if failed.
		"""

		# Validate the preamble.
		if content[:3] != bytearray([0x33, 0x79, 0x20]):
			return False

		# Validate the length and end marker.
		if content[5+content[3]:] != bytearray([0x20, 0x79, 0x33]):
			return False

		# Validate the CRC.
		if Message.crc8(content[3:-4]) != content[-4]:
			return False

		# Trim the excess now that it's validated.
		content = content[4:-4]

		mtype = int(content[0] >> 4)
		mid = int(((content[0] & 0x0F) << 8) | content[1])
		src = int(content[2])
		dst = int(content[3])

		if mtype == PING:
			return Ping(mid, src, dst)

		elif mtype == ACK:
			ver = int(content[4])
			return Ack(mid, src, dst, ver)

		return False

	def crc8(data: list):
		
		crc = 0
		for i in range(len(data)):
			crc ^= data[i]
			for j in range(8):
				if crc & 0x80:
					crc = (crc << 1) ^ 0x07
				else:
					crc <<= 1
				crc &= 0xFF

		return crc

	def make(data) -> bytes:
		return bytes([
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
		self.mtype  = 0
		self.mid    = mid
		self.src    = src
		self.dst    = dst
		super().__init__(Message.make([
			(self.mtype << 4) | (self.mid >> 8),
			self.mid & 0xFF,
			self.src, self.dst
		]))

	def info(self):
		print(f"MTYPE  : {self.mtype} (PING)")
		print(f"MID    : {self.mid}")
		print(f"SRC    : {self.src}")
		print(f"DST    : {self.dst}")

	def send(pi, bus: int, addr: int, mid: int, attempts=4, delay=0.1):
		"""
		Send a PING and return the ACK, or False if failed.
		"""

		for i in range(attempts):

			handle = pi.i2c_open(bus, addr)
			pi.i2c_write_i2c_block_data(handle, 0, Ping(mid, 0, addr).bytes())
			reply = pi.i2c_read_device(handle, 13)[1]
			message = Message.from_bytes(reply)
			if type(message) is not Ack:
				time.sleep(delay)
				continue
			pi.i2c_close(handle)
			return message

		return False

class Ack(Message):

	mtype  = None
	mid    = None
	src    = None
	dst    = None
	ver    = None

	def __init__(self, mid: int, src: int, dst: int, ver: int):
		self.mtype  = 1
		self.mid    = mid
		self.src    = src
		self.dst    = dst
		self.ver    = ver
		super().__init__(Message.make([
			(self.mtype << 4) | (self.mid >> 8),
			self.mid,
			self.src, self.dst, self.ver
		]))

	def info(self):
		print(f"MTYPE  : {self.mtype} (ACK)")
		print(f"MID    : {self.mid}")
		print(f"SRC    : {self.src}")
		print(f"DST    : {self.dst}")
		print(f"VER    : {self.ver}")

class Actuation(Message):

	mtype   = None
	mid     = None
	src     = None
	dst     = None
	values  = None

	def __init__(self, mid: int, src: int, dst: int, values: int):
		self.mtype   = 2
		self.mid     = mid
		self.src     = src
		self.dst     = dst
		self.values  = values
		super().__init__(Message.make([
			(self.mtype << 4) | (self.mid >> 8),
			self.mid,
			self.src, self.dst,
			*self.values.to_bytes(2, "big")
		]))

	def info(self):
		print(f"MTYPE  : {self.mtype} (ACTUATION)")
		print(f"MID    : {self.mid}")
		print(f"SRC    : {self.src}")
		print(f"DST    : {self.dst}")
		print(f"VALUES : {self.values}")

	def send(pi, bus: int, addr: int, mid: int, values: int, attempts=4, delay=0.1):
		"""
		Send an ACTUATION and return the ACK, or False if failed.
		"""

		for i in range(attempts):

			handle = pi.i2c_open(bus, addr)
			pi.i2c_write_i2c_block_data(handle, 0, Actuation(mid, 0, addr, values).bytes())
			reply = pi.i2c_read_device(handle, 13)[1]
			message = Message.from_bytes(reply)
			if type(message) is not Ack:
				time.sleep(delay)
				continue
			pi.i2c_close(handle)
			return message

		return False

class Tmask(Message):

	mtype  = None
	mid    = None
	src    = None
	dst    = None
	mask   = None

	def __init__(self, mid: int, src: int, dst: int, mask: int):
		self.mtype  = 3
		self.mid    = mid
		self.src    = src
		self.dst    = dst
		self.mask   = mask
		super().__init__(Message.make([
			(self.mtype << 4) | (self.mid >> 8),
			self.mid,
			self.src, self.dst,
			*self.mask.to_bytes(2, "big")
		]))

	def info(self):
		print(f"MTYPE  : {self.mtype} (TMASK)")
		print(f"MID    : {self.mid}")
		print(f"SRC    : {self.src}")
		print(f"DST    : {self.dst}")
		print(f"MASK   : {self.mask}")

class Tset(Message):

	mtype    = None
	mid      = None
	src      = None
	dst      = None
	index    = None
	delay    = None
	offTime  = None
	onTime   = None

	def __init__(self, mid: int, src: int, dst: int, index: int, delay: int,
		offTime: int, onTime: int):

		self.mtype    = 4
		self.mid      = mid
		self.src      = src
		self.dst      = dst
		self.index    = index
		self.delay    = delay
		self.offTime  = offTime
		self.onTime   = onTime
		super().__init__(Message.make([
			(self.mtype << 4) | (self.mid >> 8),
			self.mid,
			self.src, self.dst,
			self.index,
			*self.delay.to_bytes(4, "big"),
			*self.offTime.to_bytes(4, "big"),
			*self.onTime.to_bytes(4, "big"),
		]))

	def info(self):
		print(f"MTYPE     : {self.mtype} (TSET)")
		print(f"MID       : {self.mid}")
		print(f"SRC       : {self.src}")
		print(f"DST       : {self.dst}")
		print(f"INDEX     : {self.index}")
		print(f"DELAY     : {self.delay}")
		print(f"OFF_TIME  : {self.offTime}")
		print(f"ON_TIME   : {self.onTime}")

