#ifndef PROTOCOL_H
#define PROTOCOL_H

enum MTYPE
{
	PING,
	ACK,
	ACTUATION,
	TMASK,
	TSET,
};

uint8_t PREAMBLE[3] = { 0x33, 0x79, 0x20 };
uint8_t END_MARKER[3] = { 0x20, 0x79, 0x33 };

/* Safely grab just one byte from a buffer. */
byte _b(byte *buffer, uint8_t i)
{
	return buffer[i] & 0xFF;
}

/* Validate a message's preamble, end marker, length, and CRC. Return true if
   the message was successfully validated. */
bool validate_message(char *buffer, uint8_t len)
{
	/* Preamble validation. */
	for (uint8_t i = 0; i < 3; i++)
		if (_b(buffer,i) != _b(PREAMBLE,i))
			return false;

	/* Length and end marker validation. */
	for (uint8_t i = 0; i < 3; i++)
		if (_b(buffer,4+_b(buffer,3)+i) != _b(END_MARKER,i))
			return false;

	/* CRC-8 validation with standard CRC8 parameters. See crccalc.com */
	uint8_t crc = 0x00;
	for (uint8_t i = 0; i < _b(buffer,3)-1; i++)
	{
		crc ^= _b(buffer,4+i);
		for (uint8_t j = 0; j < 8; j++)
		{
			if (crc & 0x80)
				crc = (uint8_t)((crc << 1) ^ 0x07);
			else
				crc <<= 1;
		}
	}

	if (crc != _b(buffer,4+_b(buffer,3)-1))
		return false;

	return true;
}

#endif
