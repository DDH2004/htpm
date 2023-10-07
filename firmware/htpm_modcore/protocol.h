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

	/* Length-based end marker validation. */
	for (uint8_t i = 0; i < 3; i++)
		if (_b(buffer,5+_b(buffer,3)+i) != _b(END_MARKER,i))
			return false;

	/* Calculate the CRC-8 with standard CRC8 parameters. See crccalc.com */
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

	/* Check if the message was corrupted. */
	if (crc != _b(buffer,4+_b(buffer,3)))
		return false;

	/* Finally make sure that it's a valid MTYPE with the right length. */
	switch (_b(buffer,4) >> 4)
	{
		case PING:
			if (_b(buffer,3) != 0x04)
				return false;
			break;
		case ACK:
			if (_b(buffer,3) != 0x05)
				return false;
			break;
		case ACTUATION:
			if (_b(buffer,3) != 0x06)
				return false;
			break;
		case TMASK:
			if (_b(buffer,3) != 0x06)
				return false;
			break;
		case TSET:
			if (_b(buffer,3) != 0x0D)
				return false;
			break;
		default:
			return false;
	}

	return true;
}

/* Debug print the contents of a message to serial. */
void debug_print(byte *message)
{
	uint32_t buffer32 = 0;

	switch (_b(message,4) >> 4)
	{
		case PING:
			Serial.println("------------------------");
			Serial.println("MTYPE ....... PING");
			Serial.print("MID ......... ");
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
			Serial.println("MTYPE ....... ACK");
			Serial.print("MID ......... ");
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
			Serial.println("------------------------");
			Serial.println("MTYPE........ ACTUATION");
			Serial.print("MID ......... ");
			buffer32 = ((_d(message,0) & 0xF0) << 4) & _d(message,1);
			Serial.println(buffer32);
			Serial.print("SRC ......... ");
			Serial.println(_d(message,2));
			Serial.print("DST ......... ");
			Serial.println(_d(message,3));
			Serial.print("VALUES ...... ");
			buffer32 = (_d(message,4) << 8) | _d(message,5) & 0xFFFF;
			Serial.println(buffer32, HEX);
			Serial.println("------------------------");
			break;
		case TMASK:
			Serial.println("------------------------");
			Serial.println("MTYPE........ TMASK");
			Serial.print("MID ......... ");
			buffer32 = ((_d(message,0) & 0xF0) << 4) & _d(message,1);
			Serial.println(buffer32);
			Serial.print("SRC ......... ");
			Serial.println(_d(message,2));
			Serial.print("DST ......... ");
			Serial.println(_d(message,3));
			Serial.print("MASK ........ ");
			buffer32 = (_d(message,4) << 8) | _d(message,5) & 0xFFFF;
			Serial.println(buffer32, HEX);
			Serial.println("------------------------");
			break;
		case TSET:
			Serial.println("------------------------");
			Serial.println("MTYPE........ TSET");
			Serial.print("MID ......... ");
			buffer32 = ((_d(message,0) & 0xF0) << 4) & _d(message,1);
			Serial.println(buffer32);
			Serial.print("SRC ......... ");
			Serial.println(_d(message,2));
			Serial.print("DST ......... ");
			Serial.println(_d(message,3));
			Serial.print("INDEX ....... ");
			Serial.println(_d(message,4));
			Serial.print("TIMER ....... ");
			buffer32 = (_d(message,4) & 0x0F) << 8 | _d(message,5);
			buffer32 <<= 8;
			buffer32 |= _d(message,6);
			buffer32 <<= 8;
			buffer32 |= _d(message,7);
			Serial.println(buffer32, HEX);
			Serial.println("------------------------");
			break;
		default:
			Serial.println("Invalid MTYPE.");
	}
}

#endif
