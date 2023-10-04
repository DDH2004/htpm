/* HTP!m MODCORE Firmware
 * Firmware flashed onto the ATmega328 chips in HTP!m MODCOREs to actuate and
 * control up to 16 separate lines of power, receiving commands and sending
 * responses via I2C.
 */

#include <Wire.h>
#include "config.h"
#include "sr.h"

#define SER    2
#define RCLK   3
#define SRCLK  4

void receive()
{
	byte message[256] = {0};

	for (uint8_t i = 0; Wire.available() || i >= 255; i++)
		message[i] = Wire.read();
}

void setup()
{
	Serial.begin(9600);
	pinMode(SER  , OUTPUT);
	pinMode(RCLK , OUTPUT);
	pinMode(SRCLK, OUTPUT);

	Wire.begin(ADDRESS);
	Wire.onReceive(receive);

	sr_write(SER, RCLK, SRCLK, 0);
}

void loop()
{
	delay(1000);
}
