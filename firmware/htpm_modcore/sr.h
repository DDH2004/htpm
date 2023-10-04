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

void sr_write(uint16_t val)
{
	digitalWrite(RCLK, LOW);

	for (uint8_t i = 0; i < 16; i++)
	{
		digitalWrite(SER, (val >> i) & 1);
		digitalWrite(SRCLK, HIGH);
		digitalWrite(SRCLK, LOW);
	}

	digitalWrite(RCLK, HIGH);
}

#endif
