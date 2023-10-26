#ifndef PROTOCOL_H
#define PROTOCOL_H

#include "output.h"

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

/* CRC8 calculation given a buffer, starting index, and ending index. Both the
   start and end indices are inclusive. */
uint8_t crc8(byte *buffer, uint8_t start, uint8_t end)
{
	uint8_t crc = 0x00;

	for (uint8_t i = 0; i < 1+end-start; i++)
	{
		crc ^= _b(buffer,start+i);
		for (uint8_t j = 0; j < 8; j++)
		{
			if (crc & 0x80)
				crc = (uint8_t)((crc << 1) ^ 0x07);
			else
				crc <<= 1;
		}
	}

	return crc;
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

	/* Check if the message was corrupted. */
	if (crc8(buffer, 3, 3+_b(buffer,3)) != _b(buffer,4+_b(buffer,3)))
		return false;

	/* Finally, make sure that it's a valid MTYPE with the right length. */
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
			if (_b(buffer,3) != 0x0d)
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
			Serial.println("MTYPE ..... PING");
			Serial.print("MID ....... ");
			Serial.println(((_b(message,4) & 0x0F) << 8) | _b(message,5));
			Serial.print("SRC ....... ");
			p2hexln(_b(message,6));
			Serial.print("DST ....... ");
			p2hexln(_b(message,7));
			break;
		case ACK:
			Serial.println("MTYPE ..... ACK");
			Serial.print("MID ....... ");
			Serial.println(((_b(message,4) & 0x0F) << 8) | _b(message,5));
			Serial.print("SRC ....... ");
			p2hexln(_b(message,6));
			Serial.print("DST ....... ");
			p2hexln(_b(message,7));
			Serial.print("VER ....... ");
			Serial.println(_b(message,8));
			break;
		case ACTUATION:
			Serial.println("MTYPE ..... ACTUATION");
			Serial.print("MID ....... ");
			Serial.println(((_b(message,4) & 0x0F) << 8) | _b(message,5));
			Serial.print("SRC ....... ");
			p2hexln(_b(message,6));
			Serial.print("DST ....... ");
			p2hexln(_b(message,7));
			buffer32 = (uint16_t)_b(message,8) << 8 | _b(message,9);
			Serial.print("VALUES .... ");
			Serial.println(buffer32, BIN);
			break;
		case TMASK:
			break;
		case TSET:
			break;
		default:
			Serial.println("Invalid MTYPE.");
	}
}

void send_ack(uint16_t mid, uint8_t src, uint8_t dst, uint8_t ver)
{
	byte message[13];

	for (uint8_t i = 0; i < 3; i++)
		message[i] = PREAMBLE[i];

	for (uint8_t i = 10; i < 13; i++)
		message[i] = END_MARKER[i-10];

	/* Length */
	message[3] = 5;

	/* MTYPE and MID */
	message[4] = (1 << 4) | (mid >> 8);
	message[5] = mid & 0xFF;

	/* SRC, DST, and VER */
	message[6] = src;
	message[7] = dst;
	message[8] = ver;

	/* CRC */
	message[9] = crc8(message, 3, 8);

	Serial.println(">>>>>>>>");
	debug_print(message);

	Wire.write(message, 13);
}

#endif
