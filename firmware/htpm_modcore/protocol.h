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

/* Safely grab just one byte from a valid message's data section. */
byte _d(byte *message, uint8_t i)
{
	return message[4+i] & 0xFF;
}

/* Validate a message's preamble, end marker, length, and CRC. Return true if
   the message was successfully validated. */
bool validate(char *buffer, uint8_t len)
{
	/* Preamble validation. */
	for (uint8_t i = 0; i < 3; i++)
		if (_b(buffer,i) != _b(PREAMBLE,i))
			return false;

	/* Length and end marker validation. */
	for (uint8_t i = 0; i < 3; i++)
		if (_b(buffer,5+_b(buffer,3)+i) != _b(END_MARKER,i))
			return false;

	/* CRC-8 validation with standard CRC8 parameters. See crccalc.com */
	uint8_t crc = 0x00;
	for (uint8_t i = 0; i < 1+_b(buffer,3); i++)
	{
		crc ^= _b(buffer,3+i);
		for (uint8_t j = 0; j < 8; j++)
		{
			if (crc & 0x80)
				crc = (uint8_t)((crc << 1) ^ 0x07);
			else
				crc <<= 1;
		}
	}

	if (crc != _b(buffer,4+_b(buffer,3)))
		return false;

	/* Finally make sure that it's a valid MTYPE. */
	switch (_b(buffer,4) >> 4)
	{
		case PING:
		case ACK:
		case ACTUATION:
		case TMASK:
		case TSET:
			return true;
	}

	return false;
}

/* Debug print the contents of a message to serial. */
void debug_print(byte *message)
{
	uint32_t buffer32 = 0;

	switch (_b(message,4) >> 4)
	{
		case PING:
			Serial.println("------------------------");
			Serial.println("TYPE ........ PING");
			Serial.print("MSG ID ...... ");
			buffer32 = ((_d(message,0) & 0xF0) << 4) & _d(message,1);
			Serial.println(buffer32);
			Serial.print("SRC ......... ");
			Serial.println(_d(message,2));
			Serial.print("DST ......... ");
			Serial.println(_d(message,3));
			Serial.println("------------------------");
			break;
		case ACK:
			Serial.println("------------------------");
			Serial.println("TYPE ........ ACK");
			Serial.print("MSG ID ...... ");
			buffer32 = ((_d(message,0) & 0xF0) << 4) & _d(message,1);
			Serial.println(buffer32);
			Serial.print("SRC ......... ");
			Serial.println(_d(message,2));
			Serial.print("DST ......... ");
			Serial.println(_d(message,3));
			Serial.print("VER ......... ");
			Serial.println(_d(message,4));
			Serial.println("------------------------");
			break;
		case ACTUATION:
			break;
		case TMASK:
			break;
		case TSET:
			break;
		default:
			Serial.println("Invalid MTYPE.");
	}
}

#endif
