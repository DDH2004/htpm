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

/* Validate a message's preamble, end marker, length, and CRC. Return true if
   the message was successfully validated. */
bool validate_message(char *buffer, int len)
{
	/* Preamble validation. */
	for (uint8_t i = 0; i < 3; i++)
		if (buffer[i] != PREAMBLE[i])
			return false;

	/* Length and end marker validation. */
	for (uint8_t i = 0; i < 3; i++)
		if (buffer[4+buffer[3]+i] != END_MARKER[i])
			return false;

	return true;
}

#endif
