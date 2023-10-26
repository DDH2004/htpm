#ifndef SR_H
#define SR_H

enum PINS
{
	SER   = 2,
	RCLK  = 3,
	SRCLK = 4,
};

void sr_init()
{
	pinMode(SER   , OUTPUT);
	pinMode(RCLK  , OUTPUT);
	pinMode(SRCLK , OUTPUT);
}

/* Shift out 16 bits. */
void sr_write(uint16_t val)
{
	digitalWrite(RCLK, LOW);
	shiftOut(SER, SRCLK, LSBFIRST, val & 0xFF);
	shiftOut(SER, SRCLK, LSBFIRST, val >> 8);
	digitalWrite(RCLK, HIGH);
}

#endif
