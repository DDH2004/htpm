/* HTP!m MODCORE Firmware
 * Firmware flashed onto the ATmega328 chips in HTP!m MODCOREs to actuate and
 * control up to 16 separate lines of power, receiving commands and sending
 * responses via I2C.
 */

#include <Wire.h>
#include "config.h"
#include "sr.h"

void receive()
{
	byte message[256] = {0};

	for (uint8_t i = 0; Wire.available() || i >= 255; i++)
		message[i] = Wire.read();
}

void setup()
{
	Serial.begin(9600);

	Wire.begin(ADDRESS);
	Wire.onReceive(receive);

	sr_init();
	sr_write(0);
}

void loop()
{
	delay(1000);
}
